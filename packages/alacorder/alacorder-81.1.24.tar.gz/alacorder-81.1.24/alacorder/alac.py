"""
┏┓┓ ┏┓┏┓┏┓┳┓┳┓┏┓┳┓
┣┫┃ ┣┫┃ ┃┃┣┫┃┃┣ ┣┫
┛┗┗┛┛┗┗┛┗┛┛┗┻┛┗┛┛┗
(c) 2023 Sam Robson

Dependencies: Python 3.9+, Google Chrome, brotli 1.0.9+, polars 0.18.1+, pymupdf 1.21.1+, rich 13.3.3+, selenium 4.8.3+, typer 0.9.0+, xlsx2csv 0.8.1+, xlsxwriter 3.0.9+
"""

__version__ = "81.1.24"

import os
import re
import glob
import time
from datetime import datetime
from pathlib import Path
from typing_extensions import Annotated
import typer
from rich.progress import Progress, MofNCompleteColumn
from rich.console import Console
import fitz
import polars as pl
import xlsxwriter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pl.Config.set_tbl_formatting("NOTHING")
pl.Config.set_tbl_dataframe_shape_below(True)
pl.Config.set_tbl_hide_column_data_types(True)

console = Console()
app = typer.Typer(
    help="Alacorder collects case detail PDFs from Alacourt.com and processes them into data tables suitable for research purposes.",
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    add_completion=False,
)


def write(output: dict, path: str, log: bool = False):
    """
    Write each value in `output` dict {'name': pl.DataFrame} to path. If exporting multiple tables, extension must be .xls or .xlsx. Otherwise, write() supports .xls, .xlsx, .csv, .json, and .parquet.
    """

    def _write(output: dict, path: str):
        if isinstance(output, pl.DataFrame):  # convert to dict
            output = {"table": output}
        ext = os.path.splitext(path)[1]
        assert (
            ext in (".xlsx", ".xls") or len(output) == 1
        )  # multitable export only to .xlsx/.xls files
        assert ext in (
            ".xlsx",
            ".xls",
            ".csv",
            ".json",
            ".parquet",
        )  # supported file extensions only
        if ext in (".xlsx", ".xls"):
            with xlsxwriter.Workbook(path) as workbook:
                for o in output:
                    output[o].write_excel(
                        workbook=workbook, worksheet=o, autofit=True, float_precision=2
                    )
        if ext in (".parquet", ".json", ".csv"):
            output = list(output.values())[0]
            if ext == ".parquet":
                output.write_parquet(path, compression="brotli")
            if ext == ".json":
                output.write_json(path),
            if ext == ".csv":
                output.write_csv(path)

    if log:
        with console.status("Writing to output path…"):
            _write(output, path)
    else:
        _write(output, path)


def read(source, all_sheets=False):
    """
    Read input into pl.DataFrame. If directory, reads PDFs into archive df.
    """

    def extract_text(path) -> str:
        """
        From path, return full text of PDF as string (PyMuPdf engine required!)
        """
        try:
            doc = fitz.open(path)
        except:
            return ""
        text = ""
        for pg in doc:
            try:
                text += " \n ".join(
                    x[4].replace("\n", " ") for x in pg.get_text(option="blocks")
                )
            except:
                pass
        text = re.sub(r"(<image\:.+?>)", "", text).strip()
        return text

    if isinstance(source, str):
        source = os.path.abspath(source)
        if os.path.isfile(source):
            ext = os.path.splitext(source)[1]
            if ext in (".xls", ".xlsx"):
                if all_sheets:
                    output = pl.read_excel(
                        source,
                        sheet_id=0,
                        xlsx2csv_options={"ignore_errors": True},
                        read_csv_options={"ignore_errors": True},
                    )
                else:
                    output = pl.read_excel(
                        source,
                        xlsx2csv_options={"ignore_errors": True},
                        read_csv_options={"ignore_errors": True},
                    )
            if ext == ".json":
                output = pl.read_json(source)
            if ext == ".csv":
                output = pl.read_csv(source, ignore_errors=True)
            if ext == ".parquet":
                output = pl.read_parquet(source)
            if ext == ".txt":
                with open(source) as file:
                    output = file.read()
            if ext == ".pdf":
                output = extract_text(source)
        if os.path.isdir(source):
            paths = glob.glob(source + "**/*.pdf", recursive=True)
            all_text = []
            progress_bar = Progress(
                *Progress.get_default_columns(), MofNCompleteColumn()
            )
            with progress_bar as p:
                for path in p.track(paths, description="Reading PDFs…"):
                    all_text += [extract_text(path)]
            output = pl.DataFrame(
                {"Timestamp": time.time(), "AllPagesText": all_text, "Path": paths}
            )
    if isinstance(source, list):
        all_text = []
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as p:
            for path in p.track(source, description="Reading PDFs…"):
                all_text += [extract_text(path)]
        output = pl.DataFrame(
            {"Timestamp": time.time(), "AllPagesText": all_text, "Path": paths}
        )
    if isinstance(source, pl.DataFrame):
        output = source
    if isinstance(output, pl.DataFrame):
        if "CaseNumber" not in output.columns and "AllPagesText" in output.columns:
            output = output.with_columns(
                pl.concat_str(
                    [
                        pl.col("AllPagesText").str.extract(
                            r"(County: )(\d{2})", group_index=2
                        ),
                        pl.lit("-"),
                        pl.col("AllPagesText").str.extract(
                            r"(\w{2}\-\d{4}\-\d{6}\.\d{2})"
                        ),
                    ]
                ).alias("CaseNumber")
            )
        if "AllPagesText" in output.columns and "CaseNumber" in output.columns:
            output = output.unique("CaseNumber")
    return output


class AlacourtDriver:
    """
    Automates Alacourt party search results and case PDF retrieval. Initialize with path to downlaod directory, then call login() before searching.
    """

    # config
    def __init__(self, dirpath=None, headless=True, cID=None, uID=None, pwd=None):
        opt = webdriver.ChromeOptions()
        if headless:
            opt.add_argument("--headless=new")
        if dirpath != None:
            opt.add_experimental_option(
                "prefs",
                {
                    "download.default_directory": os.path.abspath(dirpath),
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True,
                },
            )
        else:
            opt.add_experimental_option(
                "prefs",
                {
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True,
                },
            )
        if dirpath != None:
            self.dirpath = os.path.abspath(dirpath)
        else:
            self.dirpath = None
        self.headless = headless
        with console.status("Starting WebDriver (requires Google Chrome)…"):
            self.driver = webdriver.Chrome(options=opt)
        self.party_search_queue = None
        self.case_number_queue = None
        self.output = None
        self.cID = cID
        self.uID = uID
        self.pwd = pwd
        if cID != None and uID != None and pwd != None:
            self.login(cID, uID, pwd)

    def login(self, cID=None, uID=None, pwd=None, log=True) -> None:
        """
        Login to Alacourt using provided credentials.
        """

        def _login(driver, cID, uID, pwd):
            driver.get("https://v2.alacourt.com")
            cID_box = driver.find_element(by=By.ID, value="ContentPlaceHolder_txtCusid")
            uID_box = driver.find_element(
                by=By.ID, value="ContentPlaceHolder_txtUserId"
            )
            pwd_box = driver.find_element(
                by=By.ID, value="ContentPlaceHolder_txtPassword"
            )
            login_button = driver.find_element(
                by=By.ID, value="ContentPlaceHolder_btLogin"
            )
            cID_box.send_keys(cID)
            uID_box.send_keys(uID)
            pwd_box.send_keys(pwd)
            login_button.click()
            continue_button = driver.find_elements(
                by=By.ID, value="ContentPlaceHolder_btnContinueLogin"
            )
            if len(continue_button) > 0:
                continue_button[0].click()
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.ID, "btnLogOff"))
                )
                return True
            except:
                raise Exception("Invalid Alacourt credentials.")

        if cID != None:
            self.cID = cID
        if uID != None:
            self.uID = uID
        if pwd != None:
            self.pwd = pwd

        if self.cID == None or self.uID == None or self.pwd == None:
            raise Exception("Must enter Alacourt credentials to login.")

        if log:
            with console.status("Logging in to Alacourt…"):
                return _login(self.driver, self.cID, self.uID, self.pwd)
        else:
            return _login(self.driver, self.cID, self.uID, self.pwd)

    # party search
    def set_party_search_queue(self, queue) -> None:
        """
        Set path to Party Search queue spreadsheet.
        """
        if isinstance(queue, pl.DataFrame):
            self.queue_path = None
            self.party_search_queue = queue
        if isinstance(queue, str):
            if os.path.isfile(queue):
                self.queue_path = queue
                self.party_search_queue = read(queue)
            else:
                raise Exception("Could not read input.")
        for col in ["Retrieved", "Timestamp", "Case Count"]:
            if col not in self.party_search_queue.columns:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.lit("").alias(col)
                )
        pscols = [
            "NAME",
            "PARTY_TYPE",
            "SSN",
            "DOB",
            "COUNTY",
            "DIVISION",
            "CASE_YEAR",
            "NO_RECORDS",
            "FILED_BEFORE",
            "FILED_AFTER",
        ]
        col_dict = {}
        for col in self.party_search_queue.columns:
            d = {re.sub(" ", "_", col.upper()): col}
            col_dict.update(d)
        for key in col_dict:
            if key in pscols:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.col(col_dict[key]).alias("TEMP_" + key)
                )
        temp_pscols = ["TEMP_" + col for col in pscols]
        for col in temp_pscols:
            if col not in self.party_search_queue.columns:
                self.party_search_queue = self.party_search_queue.with_columns(
                    pl.lit("").alias(col)
                )
        for col in self.party_search_queue.columns:
            self.party_search_queue = self.party_search_queue.with_columns(
                pl.when(pl.col(col) == None).then("").otherwise(pl.col(col)).alias(col)
            )

    def set_party_search_output(self, output_path) -> None:
        """
        Set path to Party Search output spreadsheet.
        """
        self.output = output_path

    def party_search(
        self,
        name="",
        party_type="",
        ssn="",
        dob="",
        county="",
        division="",
        case_year="",
        filed_before="",
        filed_after="",
        no_records="",
        criminal_only=False,
    ) -> None:
        """
        Alacourt Party Search with fields provided.
        """
        self.driver.implicitly_wait(10)
        try:
            if "frmIndexSearchForm" not in self.driver.current_url:
                self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")
        except:
            self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")

        if "frmlogin" in self.driver.current_url:
            self.login(log=False)
            self.driver.get("https://v2.alacourt.com/frmIndexSearchForm.aspx")

        # locators
        party_name_box = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtName"
        )
        ssn_box = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtSSN"
        )
        dob_box = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtDOB"
        )
        plaintiffs_pt_select = self.driver.find_element(
            by=By.ID, value="ContentPlaceHolder1_rdlPartyType_0"
        )
        defendants_pt_select = self.driver.find_element(
            by=By.ID, value="ContentPlaceHolder1_rdlPartyType_1"
        )
        all_pt_select = self.driver.find_element(
            by=By.ID, value="ContentPlaceHolder1_rdlPartyType_2"
        )
        division_select = Select(
            self.driver.find_element(
                by=By.ID, value="ContentPlaceHolder1_UcddlDivisions1_ddlDivision"
            )
        )
        county_select = Select(
            self.driver.find_element(by=By.ID, value="ContentPlaceHolder1_ddlCounties")
        )
        case_year_select = Select(
            self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlCaseYear"
            )
        )
        no_records_select = Select(
            self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlNumberOfRecords"
            )
        )
        filed_before_box = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtFrom"
        )
        filed_after_box = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtTo"
        )
        search_button = self.driver.find_element(by=By.ID, value="searchButton")

        # set fields
        if name != "":
            party_name_box.send_keys(name)
        if ssn != "":
            ssn_box.send_keys(ssn)
        if dob != "":
            dob_box.send_keys(dob)
        if party_type == "Plaintiffs":
            plaintiffs_pt_select.click()
        if party_type == "Defendants":
            defendants_pt_select.click()
        if party_type == "ALL":
            all_pt_select.click()
        if division == "" and not criminal_only:
            division = "All Divisions"
        if criminal_only:
            division = "Criminal Only"
        division_select.select_by_visible_text(division)
        if county != "":
            county_select.select_by_visible_text(county)
        if case_year != "":
            case_year_select.select_by_visible_text(str(case_year))
        if filed_before != "":
            filed_before_box.send_keys(filed_before)
        if filed_after != "":
            filed_after_box.send_keys(filed_after)
        if no_records != "":
            no_records_select.select_by_visible_text(str(no_records))
        else:
            no_records_select.select_by_visible_text("1000")

        # submit
        search_button.click()

        # wait for table
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ContentPlaceHolder1_dg"))
        )

    def read_results_page(self) -> pl.DataFrame:
        """
        Read current Party Search results page.
        """
        if "frmIndexSearchList" not in self.driver.current_url:
            raise Exception("Try again on party search results page.")
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        table = soup.find("table", {"id": "ContentPlaceHolder1_dg"})
        rows = table.find_all("tr")
        rows_text = []
        clean_rows = []
        for row in rows:
            cells = row.find_all("td")
            cells = [cell.text for cell in cells]
            rows_text += [cells]
        for row in rows_text:
            if len(row) > 10:
                clean_rows += [row]
        df = pl.DataFrame({"Row": clean_rows})
        if df.shape[0] > 0:
            df = df.select(
                [
                    pl.col("Row").list.get(0).alias("County"),
                    pl.col("Row").list.get(16).alias("CaseNumber"),
                    pl.col("Row").list.get(6).alias("Name"),
                    pl.col("Row").list.get(7).alias("JID"),
                    pl.col("Row").list.get(8).alias("OriginalCharge"),
                    pl.col("Row").list.get(9).alias("Bond"),
                    pl.col("Row").list.get(10).alias("DOB"),
                    pl.col("Row").list.get(11).alias("Sex"),
                    pl.col("Row").list.get(12).alias("Race"),
                    pl.col("Row").list.get(13).alias("CourtActionDate"),
                    pl.col("Row").list.get(15).alias("SSN"),
                ]
            )
        else:
            return pl.DataFrame()
        df = df.filter(pl.col("CaseNumber").is_null().is_not())
        return df

    def read_all_results(self) -> pl.DataFrame:
        """
        Read all current Party Search results pages.
        """
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            total_pages = int(
                soup.find(
                    "td", {"id": "ContentPlaceHolder1_dg_tcPageXofY"}
                ).text.split()[-1]
            )
        except:
            total_pages = 1
        df = self.read_results_page()
        for i in range(2, total_pages + 1):
            table = self.driver.find_element(by=By.ID, value="ContentPlaceHolder1_dg")
            page_select = Select(
                self.driver.find_element(
                    by=By.ID, value="ContentPlaceHolder1_dg_ddlPages"
                )
            )
            page_select.select_by_visible_text(str(i))
            WebDriverWait(self.driver, 10).until(EC.staleness_of(table))
            table = self.driver.find_element(by=By.ID, value="ContentPlaceHolder1_dg")
            df = pl.concat([df, self.read_results_page()])
        return df

    def start_party_search_queue(
        self, queue=None, output_path=None, criminal_only=False, verbose=False
    ) -> pl.DataFrame:
        """
        From `queue`, conduct Party Search and record results tables to `output_path`.
        """
        if isinstance(queue, pl.DataFrame) or isinstance(queue, str):
            self.set_party_search_queue(queue)
        elif self.party_search_queue == None:
            raise Exception("Must set party search queue to start.")
        if output_path != None:
            self.set_party_search_output(output_path)
        try:
            results_df = read(self.output)
            for col in results_df.columns:
                results_df = results_df.with_columns(pl.col(col).cast(pl.Utf8))
            print("Appending to existing table at output path.")
        except:
            results_df = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as p:
            for i, r in enumerate(
                p.track(
                    self.party_search_queue.rows(named=True),
                    description="Party searching…",
                )
            ):
                if r["Retrieved"] in ("", None):
                    if verbose:
                        p.console.log(f"#{i+1}: {r['TEMP_NAME']}")
                    try:
                        self.party_search(
                            name=r["TEMP_NAME"],
                            party_type=r["TEMP_PARTY_TYPE"],
                            ssn=r["TEMP_SSN"],
                            dob=r["TEMP_DOB"],
                            county=r["TEMP_COUNTY"],
                            division=r["TEMP_DIVISION"],
                            case_year=r["TEMP_CASE_YEAR"],
                            filed_before=r["TEMP_FILED_BEFORE"],
                            filed_after=r["TEMP_FILED_AFTER"],
                            no_records=r["TEMP_NO_RECORDS"],
                            criminal_only=criminal_only,
                        )
                        df = self.read_all_results()
                    except:
                        self.reconnect()
                        self.party_search(
                            name=r["TEMP_NAME"],
                            party_type=r["TEMP_PARTY_TYPE"],
                            ssn=r["TEMP_SSN"],
                            dob=r["TEMP_DOB"],
                            county=r["TEMP_COUNTY"],
                            division=r["TEMP_DIVISION"],
                            case_year=r["TEMP_CASE_YEAR"],
                            filed_before=r["TEMP_FILED_BEFORE"],
                            filed_after=r["TEMP_FILED_AFTER"],
                            no_records=r["TEMP_NO_RECORDS"],
                            criminal_only=criminal_only,
                        )
                        df = self.read_all_results()
                    df = df.with_columns(pl.lit(r["TEMP_NAME"]).alias("Search"))
                    for col in ["Retrieved", "Timestamp", "Destination"]:
                        if col in results_df.columns:
                            df = df.with_columns(pl.lit("").alias(col))
                    if df.shape[0] > 1:
                        results_df = pl.concat([results_df, df])
                    self.party_search_queue[i, "Retrieved"] = "Y"
                    self.party_search_queue[i, "Case Count"] = df.shape[0]
                    self.party_search_queue[i, "Timestamp"] = time.time()
                    if self.queue_path != None and i % 10 == 0:
                        write_queue = self.party_search_queue.select(
                            pl.exclude(
                                "TEMP_NAME",
                                "TEMP_PARTY_TYPE",
                                "TEMP_SSN",
                                "TEMP_DOB",
                                "TEMP_COUNTY",
                                "TEMP_DIVISION",
                                "TEMP_CASE_YEAR",
                                "TEMP_FILED_BEFORE",
                                "TEMP_FILED_AFTER",
                                "TEMP_NO_RECORDS",
                            )
                        )
                        write({"queue": write_queue}, self.queue_path)
                    if self.output != None and i % 10 == 0:
                        write({"results": results_df}, self.output)
            if self.queue_path != None:
                write_queue = self.party_search_queue.select(
                    pl.exclude(
                        "TEMP_NAME",
                        "TEMP_PARTY_TYPE",
                        "TEMP_SSN",
                        "TEMP_DOB",
                        "TEMP_COUNTY",
                        "TEMP_DIVISION",
                        "TEMP_CASE_YEAR",
                        "TEMP_FILED_BEFORE",
                        "TEMP_FILED_AFTER",
                        "TEMP_NO_RECORDS",
                    )
                )
                write({"queue": write_queue}, self.queue_path)
            if self.output != None:
                write({"results": results_df}, self.output)
        return results_df

    # case number search
    def set_case_number_queue(self, queue) -> None:
        """
        Set case number queue.
        """
        if isinstance(queue, pl.DataFrame):
            self.case_number_queue = queue
        if isinstance(queue, str):
            self.case_number_queue_path = queue
            self.case_number_queue = read(queue)
        for col in ["Retrieved", "Timestamp", "Destination"]:
            if col not in self.case_number_queue.columns:
                self.case_number_queue = self.case_number_queue.with_columns(
                    pl.lit("").alias(col)
                )
        if (
            "CaseNumber" not in self.case_number_queue.columns
            and "Case Number" in self.case_number_queue.columns
        ):
            self.case_number_queue = self.case_number_queue.with_columns(
                pl.col("Case Number").alias("CaseNumber")
            )

    def case_number_search(self, case_number="", download=True) -> bool:
        """
        Use Alacourt Case Lookup to search for a case by number. If `download` is true, will also download case detail PDF. Returns False if case detail is unavailable.
        """
        self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")

        if "frmlogin" in self.driver.current_url:
            self.login(log=False)
            self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")

        county_select = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlCounty"
        )
        division_select = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlDivision"
        )
        case_year_select = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlCaseYear"
        )
        case_number_input = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$txtCaseNumber"
        )
        case_extension_select = Select(
            self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlExt"
            )
        )
        number_of_cases_select = self.driver.find_element(
            by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlNumberOfCases"
        )
        cmap = pl.DataFrame(
            {
                "Selection": [
                    "94 - ARDMORE",
                    "93 - ATHENS",
                    "04 - AUTAUGA",
                    "05 - BALDWIN",
                    "06 - BARBOUR - CLAYTON",
                    "69 - BARBOUR - EUFAULA",
                    "89 - BERRY",
                    "07 - BIBB",
                    "08 - BLOUNT",
                    "87 - BRUNDIDGE MUNICIPAL COURT",
                    "09 - BULLOCK",
                    "10 - BUTLER",
                    "11 - CALHOUN",
                    "12 - CHAMBERS",
                    "13 - CHEROKEE",
                    "90 - CHEROKEE",
                    "14 - CHILTON",
                    "15 - CHOCTAW",
                    "16 - CLARKE",
                    "17 - CLAY",
                    "18 - CLEBURNE",
                    "19 - COFFEE - ELBA",
                    "71 - COFFEE - ENTERPRISE",
                    "20 - COLBERT",
                    "21 - CONECUH",
                    "22 - COOSA",
                    "23 - COVINGTON",
                    "24 - CRENSHAW",
                    "25 - CULLMAN",
                    "26 - DALE",
                    "27 - DALLAS",
                    "28 - DeKALB",
                    "29 - ELMORE",
                    "30 - ESCAMBIA",
                    "31 - ETOWAH",
                    "32 - FAYETTE",
                    "33 - FRANKLIN",
                    "34 - GENEVA",
                    "35 - GREENE",
                    "36 - HALE",
                    "37 - HENRY",
                    "38 - HOUSTON",
                    "39 - JACKSON",
                    "68 - JEFFERSON - BESSEMER",
                    "01 - JEFFERSON - BIRMINGHAM",
                    "40 - LAMAR",
                    "41 - LAUDERDALE",
                    "42 - LAWRENCE",
                    "43 - LEE",
                    "44 - LIMESTONE",
                    "82 - LIVINGSTON",
                    "45 - LOWNDES",
                    "46 - MACON",
                    "47 - MADISON",
                    "48 - MARENGO",
                    "49 - MARION",
                    "50 - MARSHALL",
                    "92 - MILLBROOK",
                    "02 - MOBILE",
                    "51 - MONROE",
                    "03 - MONTGOMERY",
                    "52 - MORGAN",
                    "53 - PERRY",
                    "80 - PHENIX CITY",
                    "54 - PICKENS",
                    "55 - PIKE",
                    "88 - PRATTVILLE",
                    "56 - RANDOLPH",
                    "57 - RUSSELL",
                    "58 - SHELBY",
                    "59 - ST. CLAIR - ASHVILLE",
                    "75 - ST. CLAIR - PELL CITY",
                    "81 - SUMITON MUNICIPAL COURT",
                    "60 - SUMTER",
                    "74 - TALLADEGA - SYLACAUGA",
                    "61 - TALLADEGA - TALLADEGA",
                    "70 - TALLAPOOSA - ALEX CITY",
                    "62 - TALLAPOOSA - DADEVILLE",
                    "63 - TUSCALOOSA",
                    "64 - WALKER",
                    "65 - WASHINGTON",
                    "95 - WETUMPKA MUNICIPAL COURT",
                    "66 - WILCOX",
                    "67 - WINSTON",
                ],
                "CountyNumber": [
                    "94",
                    "93",
                    "04",
                    "05",
                    "06",
                    "69",
                    "89",
                    "07",
                    "08",
                    "87",
                    "09",
                    "10",
                    "11",
                    "12",
                    "13",
                    "90",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "71",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                    "31",
                    "32",
                    "33",
                    "34",
                    "35",
                    "36",
                    "37",
                    "38",
                    "39",
                    "68",
                    "01",
                    "40",
                    "41",
                    "42",
                    "43",
                    "44",
                    "82",
                    "45",
                    "46",
                    "47",
                    "48",
                    "49",
                    "50",
                    "92",
                    "02",
                    "51",
                    "03",
                    "52",
                    "53",
                    "80",
                    "54",
                    "55",
                    "88",
                    "56",
                    "57",
                    "58",
                    "59",
                    "75",
                    "81",
                    "60",
                    "74",
                    "61",
                    "70",
                    "62",
                    "63",
                    "64",
                    "65",
                    "95",
                    "66",
                    "67",
                ],
                "County": [
                    "ARDMORE",
                    "ATHENS",
                    "AUTAUGA",
                    "BALDWIN",
                    "BARBOUR - CLAYTON",
                    "BARBOUR - EUFAULA",
                    "BERRY",
                    "BIBB",
                    "BLOUNT",
                    "BRUNDIDGE MUNICIPAL COURT",
                    "BULLOCK",
                    "BUTLER",
                    "CALHOUN",
                    "CHAMBERS",
                    "CHEROKEE",
                    "CHEROKEE",
                    "CHILTON",
                    "CHOCTAW",
                    "CLARKE",
                    "CLAY",
                    "CLEBURNE",
                    "COFFEE - ELBA",
                    "COFFEE - ENTERPRISE",
                    "COLBERT",
                    "CONECUH",
                    "COOSA",
                    "COVINGTON",
                    "CRENSHAW",
                    "CULLMAN",
                    "DALE",
                    "DALLAS",
                    "DeKALB",
                    "ELMORE",
                    "ESCAMBIA",
                    "ETOWAH",
                    "FAYETTE",
                    "FRANKLIN",
                    "GENEVA",
                    "GREENE",
                    "HALE",
                    "HENRY",
                    "HOUSTON",
                    "JACKSON",
                    "JEFFERSON - BESSEMER",
                    "JEFFERSON - BIRMINGHAM",
                    "LAMAR",
                    "LAUDERDALE",
                    "LAWRENCE",
                    "LEE",
                    "LIMESTONE",
                    "LIVINGSTON",
                    "LOWNDES",
                    "MACON",
                    "MADISON",
                    "MARENGO",
                    "MARION",
                    "MARSHALL",
                    "MILLBROOK",
                    "MOBILE",
                    "MONROE",
                    "MONTGOMERY",
                    "MORGAN",
                    "PERRY",
                    "PHENIX CITY",
                    "PICKENS",
                    "PIKE",
                    "PRATTVILLE",
                    "RANDOLPH",
                    "RUSSELL",
                    "SHELBY",
                    "ST. CLAIR - ASHVILLE",
                    "ST. CLAIR - PELL CITY",
                    "SUMITON MUNICIPAL COURT",
                    "SUMTER",
                    "TALLADEGA - SYLACAUGA",
                    "TALLADEGA - TALLADEGA",
                    "TALLAPOOSA - ALEX CITY",
                    "TALLAPOOSA - DADEVILLE",
                    "TUSCALOOSA",
                    "WALKER",
                    "WASHINGTON",
                    "WETUMPKA MUNICIPAL COURT",
                    "WILCOX",
                    "WINSTON",
                ],
            }
        )
        dmap = pl.DataFrame(
            {
                "Code": [
                    "CC",
                    "CS",
                    "CV",
                    "DC",
                    "DR",
                    "DV",
                    "EQ",
                    "JU",
                    "MC",
                    "SM",
                    "TP",
                    "TR",
                ],
                "Selection": [
                    "CC - CIRCUIT-CRIMINAL",
                    "CS - CHILD SUPPORT",
                    "CV - CIRCUIT-CIVIL",
                    "DC - DISTRICT-CRIMINAL",
                    "DR - DOMESTIC RELATIONS",
                    "DV - DISTRICT-CIVIL",
                    "EQ - EQUITY-CASES",
                    "JU - JUVENILE",
                    "MC - MUNICIPAL-CRIMINAL",
                    "SM - SMALL CLAIMS",
                    "TP - MUNICIPAL-PARKING",
                    "TR - TRAFFIC",
                ],
            }
        )
        county_number = case_number[0:2]
        division_code = case_number[3:5]
        case_year = case_number[6:10]
        six_digit = case_number[11:17]
        if len(case_number) >= 20:
            extension = case_number[18:20]
        else:
            extension = "00"
        try:
            county = (
                cmap.filter(pl.col("CountyNumber") == county_number)
                .select("Selection")
                .to_series()[0]
            )
        except:
            return False
        division = (
            dmap.filter(pl.col("Code") == division_code)
            .select("Selection")
            .to_series()[0]
        )
        county_select.send_keys(county)
        division_select.send_keys(division)
        case_year_select.send_keys(case_year)
        case_number_input.send_keys(six_digit)
        case_extension_select.select_by_visible_text(extension)
        search_button = self.driver.find_element(by=By.ID, value="searchButton")
        search_button.click()
        try:
            WebDriverWait(self.driver, 20).until(EC.staleness_of(search_button))
        except:
            self.reconnect()
            self.driver.get("https://v2.alacourt.com/frmcaselookupform.aspx")
            county_select = self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlCounty"
            )
            division_select = self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlDivision"
            )
            case_year_select = self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlCaseYear"
            )
            case_number_input = self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$txtCaseNumber"
            )
            case_extension_select = Select(
                self.driver.find_element(
                    by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlExt"
                )
            )
            number_of_cases_select = self.driver.find_element(
                by=By.NAME, value="ctl00$ContentPlaceHolder1$ddlNumberOfCases"
            )
            county_select.send_keys(county)
            division_select.send_keys(division)
            case_year_select.send_keys(case_year)
            case_number_input.send_keys(six_digit)
            case_extension_select.select_by_visible_text(extension)
            search_button = self.driver.find_element(by=By.ID, value="searchButton")
            search_button.click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(search_button))
        if download:
            if "NoCaseDetails" in self.driver.current_url:
                return False
            else:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.ID, "ContentPlaceHolder1_lnkPrint")
                        )
                    )
                except:
                    return False
                self.driver.find_element(
                    by=By.ID, value="ContentPlaceHolder1_lnkPrint"
                ).click()
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "divPrintCase"))
                )
                self.driver.find_element(by=By.ID, value="btnPrintCase").click()
                return True

    def start_case_number_queue(
        self, queue=None, verbose=False, verify=True, pre_verify=False
    ):
        """
        From a table with 'Case Number' or 'CaseNumber' column, download cases to `AlacourtDriver.dirpath`.
        """
        if pre_verify:
            if isinstance(queue, pl.DataFrame) or isinstance(queue, str):
                self.set_case_number_queue(queue)
            elif self.case_number_queue == None:
                raise Exception("Must set case number queue to start.")
            self.verify_downloads()
        loop = True
        while loop:
            if isinstance(queue, pl.DataFrame) or isinstance(queue, str):
                self.set_case_number_queue(queue)
            elif self.case_number_queue == None:
                raise Exception("Must set case number queue to start.")
            progress_bar = Progress(
                *Progress.get_default_columns(), MofNCompleteColumn()
            )
            with progress_bar as p:
                for i, r in enumerate(
                    p.track(
                        self.case_number_queue.rows(named=True),
                        description="Fetching cases…",
                    )
                ):
                    if r["Retrieved"] in ("", None):
                        if verbose:
                            p.console.log(f"#{i+1}: {r['CaseNumber']}")
                        try:
                            success = self.case_number_search(r["CaseNumber"])
                        except:
                            self.reconnect()
                            success = self.case_number_search(r["CaseNumber"])
                        if success:
                            self.case_number_queue[i, "Retrieved"] = "Y"
                            self.case_number_queue[i, "Timestamp"] = time.time()
                            self.case_number_queue[i, "Destination"] = self.dirpath
                        else:
                            self.case_number_queue[i, "Retrieved"] = "PDF Not Available"
                            self.case_number_queue[i, "Timestamp"] = time.time()
                        if self.case_number_queue_path != None and i % 10 == 0:
                            write(
                                {"queue": self.case_number_queue},
                                self.case_number_queue_path,
                            )
                if self.case_number_queue_path != None:
                    write(
                        {"queue": self.case_number_queue}, self.case_number_queue_path
                    )
            if verify:
                self.verify_downloads()
                remaining = self.case_number_queue.filter(
                    pl.col("Retrieved").is_null() | pl.col("Retrieved").eq("")
                ).shape[0]
                if remaining == 0:
                    loop = False
            else:
                loop = False

    def reconnect(self, wait=20, max_attempt=10):
        """
        Attempt to reconnect to Alacourt after `wait` seconds, up to `max_attempt` times before raising an exception.
        """
        successfully_reconnected = False
        i = 0
        while not successfully_reconnected:
            try:
                successfully_reconnected = self.login(log=False)
            except:
                i += 1
                if i == max_attempt:
                    break
                time.sleep(wait)
        if not successfully_reconnected:
            raise Exception(
                f"Failed to reconnect to Alacourt after {max_attempt} attempts."
            )

    def verify_downloads(self, queue=None):
        """
        Read case numbers from all cases in `dirpath`, and correct `queue_path` to accurately reflect progress.
        """
        if isinstance(queue, pl.DataFrame) or isinstance(queue, str):
            self.set_case_number_queue(queue)
        elif not isinstance(self.case_number_queue, pl.DataFrame):
            raise Exception("Must set case number queue to verify.")
        if self.dirpath == None:
            raise Exception("Must set download directory to verify.")
        with console.status("Verifying downloads…"):
            time.sleep(3)
            pdfs = glob.glob(self.dirpath + "**/*.pdf", recursive=True)
            case_numbers = []
            for pdf in pdfs:
                doc = fitz.open(pdf)
                text = " \n ".join(
                    x[4].replace("\n", " ") for x in doc[0].get_text(option="blocks")
                )
                cnum = (
                    re.search(r"County: (\d\d)", str(text)).group(1)
                    + "-"
                    + re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text)).group()
                )
                case_numbers += [cnum]
        self.case_number_queue = self.case_number_queue.with_columns(
            pl.when(
                pl.col("CaseNumber").is_in(case_numbers).is_not()
                & pl.col("Retrieved").ne("PDF Not Available")
            )
            .then(pl.lit(""))
            .otherwise(pl.col("Retrieved"))
            .alias("Retrieved")
        )
        self.case_number_queue = self.case_number_queue.with_columns(
            pl.when(pl.col("CaseNumber").is_in(case_numbers))
            .then(pl.lit("Y"))
            .otherwise(pl.col("Retrieved"))
            .alias("Retrieved")
        )
        self.case_number_queue = self.case_number_queue.sort(
            "Retrieved", descending=True
        )
        if self.case_number_queue_path != None:
            write({"queue": self.case_number_queue}, self.case_number_queue_path)
        remaining = self.case_number_queue.filter(
            pl.col("Retrieved").is_null() | pl.col("Retrieved").eq("")
        ).shape[0]
        if remaining > 0:
            console.print(f"{remaining} cases remaining after download verification.")
        else:
            console.print(f"All cases confirmed downloaded to destination path.")
        return self.case_number_queue


class ADOCDriver:
    """
    Collect inmate search results from the ADOC website.
    """

    def __init__(self, output_path=None, headless=True):
        if output_path != None:
            self.output = os.path.abspath(output_path)
        opt = webdriver.ChromeOptions()
        if headless:
            opt.add_argument("--headless=new")
        with console.status("Starting WebDriver (requires Google Chrome)…"):
            self.driver = webdriver.Chrome(options=opt)
        self.driver.get("https://doc.alabama.gov/inmatesearch")

    def crawl(self, output_path=None) -> pl.DataFrame:
        """
        Collect all results in ADOC Inmate Search by searching last name by letter.
        """
        if output_path != None:
            self.output = output_path
        alphabet = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        results = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as p:
            for letter in p.track(alphabet, description="Crawling ADOC…"):
                self.driver.get("https://doc.alabama.gov/inmatesearch")
                self.driver.find_element(
                    by=By.ID, value="MainContent_txtLName"
                ).send_keys(letter)
                self.driver.find_element(
                    by=By.ID, value="MainContent_btnSearch"
                ).click()
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.ID, "MainContent_gvInmateResults")
                    )
                )
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                try:
                    total_pages = int(
                        soup.find(
                            "span", {"id": "MainContent_gvInmateResults_lblPages"}
                        ).text
                    )
                except:
                    total_pages = 1
                for i in range(1, total_pages + 1):
                    soup = BeautifulSoup(self.driver.page_source, "html.parser")
                    table = soup.find("table", {"id": "MainContent_gvInmateResults"})
                    rows = table.find_all("tr")
                    rows_text = []
                    for row in rows:
                        cells = [cell.text for cell in row.find_all("td")]
                        rows_text += [cells]
                    df = pl.DataFrame({"Row": rows_text})
                    df = df.filter(pl.col("Row").list.lengths() > 3)
                    df = df.select(
                        [
                            pl.col("Row").list.get(0).alias("AIS"),
                            pl.col("Row")
                            .list.get(1)
                            .str.replace("\n", "")
                            .alias("Name"),
                            pl.col("Row").list.get(2).alias("Sex"),
                            pl.col("Row").list.get(3).alias("Race"),
                            pl.col("Row")
                            .list.get(4)
                            .cast(pl.Int64, strict=False)
                            .alias("BirthYear"),
                            pl.col("Row").list.get(5).alias("Institution"),
                            pl.col("Row")
                            .list.get(6)
                            .str.to_date("%m/%d/%Y", strict=False)
                            .alias("ReleaseDate"),
                            pl.col("Row").list.get(7).alias("Code"),
                        ]
                    )
                    results = pl.concat([results, df])
                    table_selenium = self.driver.find_element(
                        by=By.ID, value="MainContent_gvInmateResults"
                    )
                    if total_pages > 1:
                        self.driver.find_element(
                            by=By.ID, value="MainContent_gvInmateResults_btnNext"
                        ).click()
                        WebDriverWait(self.driver, 10).until(
                            EC.staleness_of(table_selenium)
                        )
                if self.output not in (None, ""):
                    write({"results": results}, self.output)
        return results

    def search(self, ais="", first_name="", last_name="") -> None:
        """
        Search ADOC Inmate Search with provided fields.
        """
        if self.driver.current_url != "https://doc.alabama.gov/InmateSearch":
            self.driver.get("https://doc.alabama.gov/InmateSearch")
        ais_box = self.driver.find_element(by=By.ID, value="MainContent_txtAIS")
        first_name_box = self.driver.find_element(
            by=By.ID, value="MainContent_txtFName"
        )
        last_name_box = self.driver.find_element(by=By.ID, value="MainContent_txtLName")
        search_button = self.driver.find_element(
            by=By.ID, value="MainContent_btnSearch"
        )
        ais_box.send_keys(ais)
        first_name_box.send_keys(first_name)
        last_name_box.send_keys(last_name)
        search_button.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "MainContent_lblMessage"))
        )

    def select_result(self, index=0) -> bool:
        """
        Select result at index from ADOC Inmate Search results table page.
        Returns false if no result at index.
        """
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        urls = soup.find_all(
            "a", {"id": re.compile(r"MainContent_gvInmateResults_lnkInmateName_\d+")}
        )
        try:
            self.driver.find_element(by=By.ID, value=urls[index]["id"]).click()
            return True
        except:
            return False

    def read_results_page(self) -> dict:
        """
        Read current Inmate History page from ADOC Inmate Search.
        """
        if "InmateHistory" not in self.driver.current_url:
            return None
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        # inmate details
        name = soup.find("span", {"id": "MainContent_DetailsView2_Label1"}).text
        ais = soup.find("span", {"id": "MainContent_DetailsView2_Label2"}).text
        institution = soup.find("span", {"id": "MainContent_DetailsView2_Label3"}).text
        details_table_text = soup.find("table", {"id": "MainContent_DetailsView1"}).text
        try:
            race = re.search(r"Race\:(.)", details_table_text).group(1)
        except:
            race = ""
        try:
            sex = re.search(r"Sex\:(.)", details_table_text).group(1)
        except:
            sex = ""
        try:
            hair_color = re.search(r"Hair Color\:([A-Z]+)", details_table_text).group(1)
        except:
            hair_color = ""
        try:
            eye_color = re.search(r"Eye Color\:([A-Z]+)", details_table_text).group(1)
        except:
            eye_color = ""
        try:
            height = re.search(r"Height\:(.+)", details_table_text).group(1)
        except:
            height = ""
        try:
            weight = re.search(r"Weight\:(.+)", details_table_text).group(1)
        except:
            weight = ""
        try:
            birth_year = re.search(r"Birth Year\:(.+)", details_table_text).group(1)
        except:
            birth_year = ""
        try:
            custody = re.search(r"Custody\n\n(.+)", details_table_text).group(1).strip()
        except:
            custody = ""
        aliases = "; ".join(
            [
                re.sub('"|,', "", cell.text).strip()
                for cell in soup.find_all(
                    "span", {"id": re.compile(r"MainContent_lvAlias_AliasLabel0_\d")}
                )
            ]
        )
        aliases = re.sub("No known Aliases", "", aliases)
        scars_marks_tattoos = "; ".join(
            [
                re.sub('"|,', "", cell.text).strip()
                for cell in soup.find_all(
                    "span", {"id": re.compile(r"MainContent_lvScars_descriptLabel_\d")}
                )
            ]
        )
        scars_marks_tattoos = re.sub(
            "No known scars marks or tattoos", "", scars_marks_tattoos
        )
        inmate_details_df = pl.DataFrame(
            {
                "Name": [name],
                "AIS": [ais],
                "Institution": [institution],
                "Race": [race],
                "Sex": [sex],
                "HairColor": [hair_color],
                "EyeColor": [eye_color],
                "Height": [height],
                "Weight": [int(weight)],
                "BirthYear": [int(birth_year)],
                "Custody": [custody],
                "Aliases": [aliases],
                "ScarsMarksTattoos": [scars_marks_tattoos],
            }
        )
        # black header "Sentences" tables
        black_tables = soup.find_all(
            "table", {"id": re.compile(r"MainContent_gvSentence_GridView1_\d+")}
        )
        black_tables_df = pl.DataFrame()
        for i, black_table in enumerate(black_tables):
            rows = black_table.find_all("tr")
            table_list = []
            for row in rows:
                table_list += [[cell.text for cell in row.find_all("td")]]
            df = pl.DataFrame({"Row": table_list})
            df = df.select(
                [
                    pl.lit(ais).alias("AIS"),
                    pl.lit(name).alias("Name"),
                    pl.lit(i + 1).alias("TableNo").cast(pl.Int64, strict=False),
                    pl.col("Row")
                    .list.get(0)
                    .str.replace_all(r"\n", "")
                    .alias("CaseNo"),
                    pl.col("Row")
                    .list.get(1)
                    .str.replace_all(r"\n", "")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("Sentenced"),
                    pl.col("Row")
                    .list.get(2)
                    .str.replace_all(r"\n", "")
                    .str.strip()
                    .alias("Offense"),
                    pl.col("Row").list.get(3).str.replace_all(r"\n", "").alias("Term"),
                    pl.col("Row")
                    .list.get(4)
                    .str.replace_all(r"\n", "")
                    .cast(pl.Int64, strict=False)
                    .alias("JailCredit"),
                    pl.col("Row")
                    .list.get(5)
                    .str.replace_all(r"\n", "")
                    .cast(pl.Int64, strict=False)
                    .alias("PreTimeServed"),
                    pl.col("Row").list.get(6).str.replace_all(r"\n", "").alias("Type"),
                    pl.col("Row")
                    .list.get(7)
                    .str.replace_all(r"\n", "")
                    .alias("CommitCounty"),
                ]
            )
            df = df.filter(pl.col("CaseNo").is_null().is_not())
            black_tables_df = pl.concat([black_tables_df, df])
        # blue header tables
        table = soup.find("table", {"id": "MainContent_gvSentence"})
        rows = table.find_all("tr")
        blue_tables_df = pl.DataFrame()
        start_blue_row = False
        table_no = 0
        for row in rows:
            if "SUFAdmit" in row.text:
                start_blue_row = True
                table_no += 1
            elif start_blue_row and "Case No." not in row.text:
                cells = [cell.text for cell in row.find_all("td")]
                df = pl.DataFrame({"TableNo": [table_no], "Row": [cells]})
                blue_tables_df = pl.concat([blue_tables_df, df])
            elif "Case No." in row.text:
                start_blue_row = False
        blue_tables_df = blue_tables_df.select(
            [
                pl.lit(name).alias("Name"),
                pl.lit(ais).alias("AIS"),
                pl.col("TableNo"),
                pl.col("Row").list.get(0).alias("SUF"),
                pl.col("Row")
                .list.get(1)
                .alias("AdmitDate")
                .str.to_date("%m/%d/%Y", strict=False),
                pl.col("Row").list.get(2).alias("TotalTerm"),
                pl.col("Row").list.get(3).alias("TimeServed"),
                pl.col("Row")
                .list.get(4)
                .alias("JailCredit")
                .cast(pl.Int64, strict=False),
                pl.col("Row").list.get(5).alias("GoodTimeReceived"),
                pl.col("Row").list.get(6).alias("GoodTimeRevoked"),
                pl.col("Row")
                .list.get(7)
                .alias("MinReleaseDate")
                .str.to_date("%m/%d/%Y", strict=False),
                pl.col("Row")
                .list.get(8)
                .alias("ParoleConsiderationDate")
                .str.to_date("%m/%d/%Y", strict=False),
                pl.col("Row").list.get(9).alias("ParoleStatus"),
            ]
        )
        return {
            "InmateDetails": inmate_details_df,
            "BlueTables": blue_tables_df,
            "BlackTables": black_tables_df,
        }

    def set_output_path(self, output_path) -> None:
        """
        Set results output path for start_queue().
        """
        self.output = output_path

    def set_queue(self, queue, output_path="") -> None:
        """
        Set queue from dataframe or spreadsheet with "Last Name", "First Name", and "AIS" columns.
        """
        if isinstance(queue, str):
            self.queue_path = queue
            self.queue = read(queue)
        if isinstance(queue, pl.DataFrame):
            self.queue_path = None
            self.queue = queue
        for col in ["Retrieved", "Timestamp"]:
            if col not in self.queue.columns:
                self.queue = self.queue.with_columns(pl.lit("").alias(col))
        for col in self.queue.columns:
            if re.sub(" ", "_", col).upper() in ["LAST_NAME", "FIRST_NAME", "AIS"]:
                self.queue = self.queue.with_columns(
                    pl.col(col).alias(f"TEMP_{re.sub(' ','_', col).upper()}")
                )
        if (
            "TEMP_LAST_NAME" not in self.queue.columns
            and "TEMP_FIRST_NAME" not in self.queue.columns
            and "Name" in self.queue.columns
        ):
            self.queue = self.queue.with_columns(
                [
                    pl.col("Name").str.extract(r"([A-Z]+)").alias("TEMP_LAST_NAME"),
                    pl.col("Name").str.extract(r" ([A-Z]+)").alias("TEMP_FIRST_NAME"),
                ]
            )
        for col in ["TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS"]:
            if col not in self.queue.columns:
                self.queue = self.queue.with_columns(pl.lit("").alias(col))

    def start_queue(self, queue=None, output_path=None, verbose=False):
        """
        ADOC Inmate Search for each in `queue`, and save results to `output_path`.
        """
        if isinstance(queue, pl.DataFrame) or isinstance(queue, str):
            self.set_queue(queue)
        elif self.queue == None:
            raise Exception("Must set queue to start.")
        if output_path != None:
            self.set_output_path(output_path)
        try:
            inmate_details = pl.read_excel(
                self.output, sheet_name="inmate-details"
            ).with_columns(pl.col("AIS").cast(pl.Utf8))
            blue_tables = pl.read_excel(
                self.output, sheet_name="blue-tables"
            ).with_columns(
                [
                    pl.col("AIS").cast(pl.Utf8),
                    pl.col("TableNo").cast(pl.Int64, strict=False),
                    pl.col("AdmitDate").str.to_date("%Y-%m-%d", strict=False),
                    pl.col("MinReleaseDate").str.to_date("%Y-%m-%d", strict=False),
                    pl.col("ParoleConsiderationDate").str.to_date(
                        "%Y-%m-%d", strict=False
                    ),
                ]
            )
            black_tables = pl.read_excel(
                self.output, sheet_name="black-tables"
            ).with_columns(
                [
                    pl.col("AIS").cast(pl.Utf8),
                    pl.col("TableNo").cast(pl.Int64, strict=False),
                    pl.col("Sentenced").str.to_date("%Y-%m-%d", strict=False),
                ]
            )
            print("Appending to existing tables at output path.")
        except:
            inmate_details = pl.DataFrame()
            blue_tables = pl.DataFrame()
            black_tables = pl.DataFrame()
        progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
        with progress_bar as p:
            for i, r in enumerate(
                p.track(self.queue.rows(named=True), description="Searching ADOC…")
            ):
                if r["Retrieved"] in (None, ""):
                    if verbose:
                        p.console.log(
                            f"#{i+1}: {r['TEMP_AIS']} {r['TEMP_FIRST_NAME']} {r['TEMP_LAST_NAME']}"
                        )
                    self.search(
                        ais=r["TEMP_AIS"],
                        first_name=r["TEMP_FIRST_NAME"],
                        last_name=r["TEMP_LAST_NAME"],
                    )
                    if self.select_result(0):
                        results = self.read_results_page()
                        inmate_details = pl.concat(
                            [inmate_details, results["InmateDetails"]]
                        )
                        blue_tables = pl.concat([blue_tables, results["BlueTables"]])
                        black_tables = pl.concat([black_tables, results["BlackTables"]])
                        self.queue[i, "Retrieved"] = "Y"
                        self.queue[i, "Timestamp"] = time.time()
                    else:
                        self.queue[i, "Retrieved"] = "NO RESULTS"
                        self.queue[i, "Timestamp"] = time.time()
                    if self.output != None and i % 10 == 0:
                        write(
                            {
                                "inmate-details": inmate_details,
                                "blue-tables": blue_tables,
                                "black-tables": black_tables,
                            },
                            self.output,
                        )
                    if self.queue_path != None and i % 10 == 0:
                        write_queue = self.queue.select(
                            pl.exclude("TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS")
                        )
                        write({"queue": write_queue}, self.queue_path)
            if self.output != None:
                write(
                    {
                        "inmate-details": inmate_details,
                        "blue-tables": blue_tables,
                        "black-tables": black_tables,
                    },
                    self.output,
                )
            if self.queue_path != None:
                write_queue = self.queue.select(
                    pl.exclude("TEMP_LAST_NAME", "TEMP_FIRST_NAME", "TEMP_AIS")
                )
                write({"queue": write_queue}, self.queue_path)
        return {
            "inmate-details": inmate_details,
            "blue-tables": blue_tables,
            "black-tables": black_tables,
        }


class Cases:
    """
    From a case archive or directory of PDF cases, create, manipulate, and export data tables.
    """

    def __init__(self, archive):
        if isinstance(archive, str):
            if os.path.isdir(archive):
                self.archive = archive
                self.is_read = False
            elif os.path.isfile(archive):
                with console.status("Reading input…"):
                    self.archive = read(archive)
                self.is_read = True
            else:
                raise Exception("Could not read input.")
        if isinstance(archive, pl.DataFrame):
            self.archive = read(archive)
            self.is_read = True
        self._cases = None
        self._fees = None
        self._filing_charges = None
        self._disposition_charges = None
        self._sentences = None
        self._financial_history = None
        self._settings = None
        self._case_action_summary = None
        self._witnesses = None
        self._attorneys = None
        self._images = None
        self._restitution = None
        self._linked_cases = None
        self._continuances = None

    def __repr__(self):
        return self.archive.select("CaseNumber").__str__()

    def read(self):
        """
        Read input into pl.DataFrame. If directory, reads PDFs into archive df.
        """
        self.archive = read(self.archive)
        self.is_read = True
        return self.archive

    def cases(self, debug=False):
        """
        Make case information table.
        """
        if debug:
            self._cases = None
        # if previously called with debug=True, reset
        if isinstance(self._cases, pl.DataFrame):
            if "D999RAW" in self._cases.columns:
                self._cases = None
        if isinstance(self._cases, pl.DataFrame):
            return self._cases
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing cases table…"):
                cases = self.archive.with_columns(
                    [
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                            group_index=1,
                        )
                        .str.replace("Case Number:", "", literal=True)
                        .str.replace(r"C$", "")
                        .str.strip()
                        .alias("Name"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)(SSN\:)(.{0,100})(Alias 1)", group_index=2)
                        .str.replace("\n", "")
                        .str.strip()
                        .alias("Alias"),
                        pl.col("AllPagesText")
                        .str.extract(r"Alias 2: (.+)")
                        .str.strip()
                        .alias("Alias2"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", group_index=1
                        )
                        .str.replace(r"[^\d/]", "")  # _all
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DOB"),
                        pl.concat_str(
                            [
                                pl.col("AllPagesText").str.extract(
                                    r"(County: )(\d{2})", group_index=2
                                ),
                                pl.lit("-"),
                                pl.col("AllPagesText").str.extract(
                                    r"(\w{2}\-\d{4}\-\d{6}\.\d{2})"
                                ),
                            ]
                        ).alias("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"(Phone: )(.+)", group_index=2)
                        .str.replace_all(r"[^0-9]", "")
                        .str.slice(0, 10)
                        .str.replace(r"(.{3}0000000)", "")
                        .alias("RE_Phone"),
                        pl.col("AllPagesText")
                        .str.extract(r"(B|W|H|A)/(?:F|M)")
                        .cast(pl.Categorical)
                        .alias("Race"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:B|W|H|A)/(F|M)")
                        .cast(pl.Categorical)
                        .alias("Sex"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:Address 1:)(.+)(?:Phone)*?", group_index=1)
                        .str.replace(r"(Phone.+)", "")
                        .str.strip()
                        .alias("Address1"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:Address 2:)(.+)")
                        .str.strip()
                        .alias("Address2"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:Zip: )(.+)", group_index=1)
                        .str.replace(r"[A-Za-z\:\s]+", "")
                        .str.strip()
                        .alias("ZipCode"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:City: )(.*)(?:State: )(.*)", group_index=1)
                        .str.strip()
                        .alias("City"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?:City: )(.*)(?:State: )(.*)", group_index=2)
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("State"),
                        pl.col("AllPagesText")
                        .str.extract(r"(Total:.+\$[^\n]*)")
                        .str.replace_all(r"[^0-9|\.|\s|\$]", "")
                        .str.extract_all(r"\s\$\d+\.\d{2}")
                        .alias("TOTALS"),
                        pl.col("AllPagesText")
                        .str.extract(r"(ACTIVE[^\n]+D999[^\n]+)")
                        .str.extract_all(r"\$\d+\.\d{2}")
                        .list.get(-1)
                        .str.replace(r"[\$\s]", "")
                        .cast(pl.Float64, strict=False)
                        .alias("D999RAW"),
                        pl.col("AllPagesText")
                        .str.extract(r"Related Cases: (.+)")
                        .str.strip()
                        .alias("RelatedCases"),
                        pl.col("AllPagesText")
                        .str.extract(r"Filing Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("FilingDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Case Initiation Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("CaseInitiationDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Arrest Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("ArrestDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Offense Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("OffenseDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Indictment Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("IndictmentDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Youthful Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("YouthfulDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"(\d+)\s*\n\s*Youthful Date:")
                        .str.strip()
                        .alias("ALInstitutionalServiceNum"),
                        pl.col("AllPagesText")
                        .str.extract(r"Alacourt\.com (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Retrieved"),
                        pl.col("AllPagesText")
                        .str.extract(r"Jury Demand: ([A-Za-z]+)")
                        .cast(pl.Categorical)
                        .alias("JuryDemand"),
                        pl.col("AllPagesText")
                        .str.extract(r"Grand Jury Court Action:(.+)")
                        .str.replace(r"Inpatient.+", "")
                        .str.strip()
                        .alias("GrandJuryCourtAction"),
                        pl.col("AllPagesText")
                        .str.extract(r"Inpatient Treatment Ordered: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("InpatientTreatmentOrdered"),
                        pl.col("AllPagesText")
                        .str.extract(r"Trial Type: ([A-Z\s]+)")
                        .str.replace(r"\n?\s*P$", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("TrialType"),
                        pl.col("AllPagesText")
                        .str.extract(r"Case Number: (.+)\s*\n*\s*County:")
                        .str.strip()
                        .alias("County"),
                        pl.col("AllPagesText")
                        .str.extract(r"Judge: (.+)")
                        .str.rstrip("T")
                        .str.strip()
                        .alias("Judge"),
                        pl.col("AllPagesText")
                        .str.extract(r"Probation Office \#: ([0-9\-]+)")
                        .alias("ProbationOffice#"),
                        pl.col("AllPagesText")
                        .str.extract(r"Defendant Status: ([A-Z\s]+)")
                        .str.rstrip("J")
                        .str.replace(r"\n", " ")
                        .str.replace(r"\s+", " ")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("DefendantStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"([^0-9]+) Arresting Agency Type:")
                        .str.replace(r"^\-.+", "")
                        .str.replace(r"County\:", "")
                        .str.replace(r"Defendant Status\:", "")
                        .str.replace(r"Judge\:", "")
                        .str.replace(r"Trial Type\:", "")
                        .str.replace(r"Probation Office \#\:", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("ArrestingAgencyType"),
                        pl.col("AllPagesText")
                        .str.extract(r"(.+) City Code/Name")
                        .str.strip()
                        .alias("CityCodeName"),
                        pl.col("AllPagesText")
                        .str.extract(r"Arresting Officer: (.+)")
                        .str.strip()
                        .alias("ArrestingOfficer"),
                        pl.col("AllPagesText")
                        .str.extract(r"Grand Jury: (.+)")
                        .str.strip()
                        .alias("GrandJury"),
                        pl.col("AllPagesText")
                        .str.extract(r"Probation Office Name: ([A-Z0-9]+)")
                        .alias("ProbationOfficeName"),
                        pl.col("AllPagesText")
                        .str.extract(r"Traffic Citation \#: (.+)")
                        .str.strip()
                        .alias("TrafficCitation#"),
                        pl.col("AllPagesText")
                        .str.extract(r"DL Destroy Date: (.+?)Traffic Citation #:")
                        .str.strip()
                        .alias("DLDestroyDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Previous DUI Convictions: (\d{3})")
                        .str.strip()
                        .cast(pl.Int64, strict=False)
                        .alias("PreviousDUIConvictions"),
                        pl.col("AllPagesText")
                        .str.extract(r"Case Initiation Type: ([A-Z\s]+)")
                        .str.rstrip("J")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("CaseInitiationType"),
                        pl.col("AllPagesText")
                        .str.extract(r"Domestic Violence: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("DomesticViolence"),
                        pl.col("AllPagesText")
                        .str.extract(r"Agency ORI: (.+)")
                        .str.replace(r"\n", "")
                        .str.replace_all(r"\s+", " ")
                        .str.strip()
                        .alias("AgencyORI"),
                        pl.col("AllPagesText")
                        .str.extract(r"Driver License N°: (.+)")
                        .str.strip()
                        .alias("DriverLicenseNo"),
                        pl.col("AllPagesText")
                        .str.extract(r"([X\d]{3}-[X\d]{2}-[X\d]{4})")
                        .alias("SSN"),
                        pl.col("AllPagesText")
                        .str.extract(r"([A-Z0-9]{11}?) State ID:")
                        .alias("StateID"),
                        pl.col("AllPagesText")
                        .str.extract(r"Weight: (\d*)", group_index=1)
                        .cast(pl.Int64, strict=False)
                        .alias("Weight"),
                        pl.col("AllPagesText")
                        .str.extract(r"Height ?: (\d'\d{2}\")")
                        .alias("Height"),
                        pl.col("AllPagesText")
                        .str.extract(r"Eyes/Hair: (\w{3})/(\w{3})", group_index=1)
                        .alias("Eyes"),
                        pl.col("AllPagesText")
                        .str.extract(r"Eyes/Hair: (\w{3})/(\w{3})", group_index=2)
                        .alias("Hair"),
                        pl.col("AllPagesText")
                        .str.extract(r"Country: (\w*+)")
                        .str.replace(r"(Enforcement|Party)", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("Country"),
                        pl.col("AllPagesText")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d) Warrant Issuance Date:")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("WarrantIssuanceDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Action Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("WarrantActionDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Issuance Status: (\w+)")
                        .str.replace(r"Description", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("WarrantIssuanceStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Action Status: (\w+)")
                        .str.replace(r"Description", "")
                        .str.strip()
                        .alias("WarrantActionStatus"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Warrant Location Date: (.+?)Warrant Location Status:"
                        )
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("WarrantLocationDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Location Status: (\w+)")
                        .str.replace(r"Description", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("WarrantLocationStatus"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)",
                            group_index=1,
                        )
                        .str.extract(
                            r"(ALIAS WARRANT|BENCH WARRANT|FAILURE TO PAY WARRANT|PROBATION WARRANT)"
                        )
                        .alias("WarrantIssuanceDescription"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)",
                            group_index=1,
                        )
                        .str.extract(
                            r"(WARRANT RECALLED|WARRANT DELAYED|WARRANT RETURNED|WARRANT SERVED)"
                        )
                        .alias("WarrantActionDescription"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)",
                            group_index=1,
                        )
                        .str.extract(r"(CLERK'S OFFICE|LAW ENFORCEMENT)")
                        .alias("WarrantLocationDescription"),
                        pl.col("AllPagesText")
                        .str.extract(r"Number Of Warrants: (\d{3}\s\d{3})")
                        .str.strip()
                        .alias("NumberOfWarrants"),
                        pl.col("AllPagesText")
                        .str.extract(r"Bond Type: (\w+)")  # +
                        .str.replace(r"Bond", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("BondType"),
                        pl.col("AllPagesText")
                        .str.extract(r"Bond Type Desc: ([A-Z\s]+)")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("BondTypeDesc"),
                        pl.col("AllPagesText")
                        .str.extract(r"([\d\.]+) Bond Amount:")
                        .cast(pl.Float64, strict=False)
                        .alias("BondAmount"),
                        pl.col("AllPagesText")
                        .str.extract(r"Bond Company: ([A-Z0-9]+)")
                        .str.rstrip("S")
                        .alias("BondCompany"),
                        pl.col("AllPagesText")
                        .str.extract(r"Surety Code: (.+)")
                        .str.replace(r"Release.+", "")
                        .str.strip()
                        .alias("SuretyCode"),
                        pl.col("AllPagesText")
                        .str.extract(r"Release Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("BondReleaseDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Failed to Appear Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("FailedToAppearDate"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Bondsman Process Issuance: ([^\n]*?) Bondsman Process Return:"
                        )
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("BondsmanProcessIssuance"),
                        pl.col("AllPagesText")
                        .str.extract(r"Bondsman Process Return: (.+)")
                        .str.replace(r"Number.+", "")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("BondsmanProcessReturn"),
                        pl.col("AllPagesText")
                        .str.extract(r"([\n\s/\d]*?) Appeal Court:")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("AppealDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"([A-Z\-\s]+) Appeal Case Number")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("AppealCourt"),
                        pl.col("AllPagesText")
                        .str.extract(r"Orgin Of Appeal: ([A-Z\-\s]+)")
                        .str.rstrip("L")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("OriginOfAppeal"),
                        pl.col("AllPagesText")
                        .str.extract(r"Appeal To Desc: ([A-Z\-\s]+)")
                        .str.replace(r"[\s\n]+[A-Z0-9]$", "")
                        .str.rstrip("O")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("AppealToDesc"),
                        pl.col("AllPagesText")
                        .str.extract(r"Appeal Status: ([A-Z\-\s]+)")
                        .str.rstrip("A")
                        .str.replace_all(r"\n", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("AppealStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"Appeal To: (\w*) Appeal")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("AppealTo"),
                        pl.col("AllPagesText")
                        .str.extract(r"LowerCourt Appeal Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.replace_all(r"[\n\s:\-]", "")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("LowerCourtAppealDate"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Disposition Date Of Appeal: (\d\d?/\d\d?/\d\d\d\d)"
                        )
                        .str.replace_all(r"[\n\s:\-]", "")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DispositionDateOfAppeal"),
                        pl.col("AllPagesText")
                        .str.extract(r"Disposition Type Of Appeal: [^A-Za-z]+")
                        .str.replace_all(r"[\n\s:\-]", "")
                        .str.strip()
                        .alias("DispositionTypeOfAppeal"),
                        pl.col("AllPagesText")
                        .str.extract(r"Number of Subponeas: (\d{3})")
                        .str.replace_all(r"[^0-9]", "")
                        .str.strip()
                        .cast(pl.Int64, strict=False)
                        .alias("NumberOfSubpoenas"),
                        pl.col("AllPagesText")
                        .str.extract(r"Updated By: (\w{3})")
                        .str.strip()
                        .alias("AdminUpdatedBy"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Transfer to Admin Doc Date: (\d\d?/\d\d?/\d\d\d\d)"
                        )
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("TransferToAdminDocDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Transfer Reason: (.+?)Transfer Desc:")
                        .str.strip()
                        .alias("TransferReason"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Administrative Information.+?Last Update: (\d\d?/\d\d?/\d\d\d\d)"
                        )
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("AdminLastUpdate"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Transfer Desc: ([A-Z\s]{0,15} \d\d?/\d\d?/\d\d\d\d)"
                        )
                        .str.replace_all(r"(Transfer Desc:)", "")
                        .str.strip()
                        .alias("TransferDesc"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Date Trial Began but No Verdict \(TBNV1\): ([^\n]+)"
                        )
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("TBNV1"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Date Trial Began but No Verdict \(TBNV2\): ([^\n]+)"
                        )
                        .str.replace(r"Financial", "")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("TBNV2"),
                        pl.col("AllPagesText")
                        .str.extract(r"TurnOver Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("TurnOverDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"TurnOver Amt\: \$(\d+\.\d\d)")
                        .cast(pl.Float64, strict=False)
                        .alias("TurnOverAmt"),
                        pl.col("AllPagesText")
                        .str.extract(r"Frequency Amt\: \$(\d+\.\d\d)")
                        .cast(pl.Float64, strict=False)
                        .alias("FrequencyAmt"),
                        pl.col("AllPagesText")
                        .str.extract(r"Due Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DueDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Over/Under Paid: \$(\d+\.\d\d)")
                        .str.replace(r",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("OverUnderPaid"),
                        pl.col("AllPagesText")
                        .str.extract(r"Last Paid Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("LastPaidDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Payor\: ([A-Z0-9]{4})")
                        .cast(pl.Categorical)
                        .alias("Payor"),
                        pl.col("AllPagesText")
                        .str.extract(r"Enforcement Status\: ([A-Z\:,\s]+)")
                        .str.replace_all(r"\s+", " ")
                        .str.replace(r" F$", "")
                        .str.strip()
                        .cast(pl.Categorical)
                        .alias("EnforcementStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"Frequency\: ([W|M])")
                        .str.replace(r"Cost Paid By\:", "")
                        .str.strip()
                        .alias("Frequency"),
                        pl.col("AllPagesText")
                        .str.extract(r"Placement Status\: (.+)")
                        .str.strip()
                        .alias("PlacementStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"PreTrial\: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("PreTrial"),
                        pl.col("AllPagesText")
                        .str.extract(r"PreTrail Date\: (.+)PreTrial")
                        .str.strip()
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("PreTrialDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"PreTrial Terms\: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("PreTrialTerms"),
                        pl.col("AllPagesText")
                        .str.extract(r"Pre Terms Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("PreTermsDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Delinquent\: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("Delinquent"),
                        pl.col("AllPagesText")
                        .str.extract(r"Delinquent Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DelinquentDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"DA Mailer\: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("DAMailer"),
                        pl.col("AllPagesText")
                        .str.extract(r"DA Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DAMailerDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Mailer\: (YES|NO)")
                        .cast(pl.Categorical)
                        .alias("WarrantMailer"),
                        pl.col("AllPagesText")
                        .str.extract(r"Warrant Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("WarrantMailerDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Last Update\: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("EnforcementLastUpdate"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Comments: (.+?)\n Over/Under Paid")
                        .str.replace(r"(?s)Warrant Mailer.+", "")
                        .str.strip()
                        .alias("EnforcementComments"),
                        pl.col("AllPagesText")
                        .str.extract(r"Updated By\: ([A-Z]{3})")
                        .alias("EnforcementUpdatedBy"),
                        pl.col("AllPagesText")
                        .str.extract(r"Appeal Case Number: (.+)")
                        .str.strip()
                        .alias("AppealCaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"Continuance Date\s*\n*\s*(\d\d/\d\d/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("ContinuanceDate"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Continuance Reason\s*\n*\s*([A-Z0-9]{2}/[A-Z0-9]{2}/[A-Z0-9]{4})"
                        )
                        .alias("ContinuanceReason"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Description:(.+?)Number of Previous Continuances:"
                        )
                        .str.strip()
                        .alias("ContinuanceDescription"),
                        pl.col("AllPagesText")
                        .str.extract(r"Number of Previous Continuances:\s*\n*\s(\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("NumberOfPreviousContinuances"),
                        pl.col("AllPagesText")
                        .str.contains(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                        .alias("HasFeeSheet"),
                    ]
                )
                # blank county
                cases = cases.with_columns(
                    pl.when(pl.col("County").eq("") | pl.col("County").is_null())
                    .then(
                        pl.col("AllPagesText").str.extract(
                            r"\w\w-\d\d\d\d-\d\d\d\d\d\d\.\d\d (.+?) Case Number"
                        )
                    )
                    .otherwise(pl.col("County"))
                    .alias("County")
                )
                # TR only fields
                cases = cases.with_columns(
                    [
                        pl.col("AllPagesText")
                        .str.extract(r"Suspension Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("SuspensionDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Speed: (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Speed"),
                        pl.col("AllPagesText")
                        .str.extract(r"Completion Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("CompletionDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Clear Date: (\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("ClearDate"),
                        pl.col("AllPagesText")
                        .str.extract(r"Speed Limit: (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("SpeedLimit"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Blood Alcohol Content: Completion Date: ?(\d\d?/\d\d?/\d\d\d\d)? (\d+\.\d\d\d)",
                            group_index=2,
                        )
                        .cast(pl.Float64, strict=False)
                        .alias("BloodAlcoholContent"),
                        pl.col("AllPagesText")
                        .str.extract(r"Ticket Number: (.+)")
                        .str.strip()
                        .alias("TicketNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"Rule 20: (.+?) Clear Date:")
                        .str.strip()
                        .alias("Rule20"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Collection Status: (.+?) \d\d?/\d\d?/\d\d\d\d"
                        )
                        .str.replace(r"\n", "")
                        .str.replace_all(r"\s+", " ")
                        .str.strip()
                        .alias("CollectionStatus"),
                        pl.col("AllPagesText")
                        .str.extract(r"Tag Number: (.+?) Vehicle Desc:")
                        .str.strip()
                        .alias("VehicleDesc"),
                        pl.col("AllPagesText")
                        .str.extract(r"Vehicle State: (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("VehicleState"),
                        pl.col("AllPagesText")
                        .str.extract(r"Driver License Class: (.+)")
                        .str.replace(r"/.+", "")
                        .str.strip()
                        .alias("DriverLicenseClass"),
                        pl.col("AllPagesText")
                        .str.extract(r"Commercial Vehicle: (YES|NO|UNKNOWN)")
                        .alias("CommercialVehicle"),
                        pl.col("AllPagesText")
                        .str.extract(r"([A-Z0-9]+) Tag Number:")
                        .alias("TagNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"Vehicle Year: (.+?) ?Vehicle State:")
                        .str.strip()
                        .alias("VehicleYear"),
                        pl.col("AllPagesText")
                        .str.extract(r"(YES|NO) Passengers Present:")
                        .alias("PassengersPresent"),
                        pl.col("AllPagesText")
                        .str.extract(r"Commercial Driver License Required: (YES|NO)")
                        .alias("CommercialDriverLicenseRequired"),
                        pl.col("AllPagesText")
                        .str.extract(r"Hazardous Materials: (YES|NO)")
                        .alias("HazardousMaterials"),
                    ]
                )
                cases = cases.with_columns(
                    [
                        pl.when(pl.col("D999RAW").is_null())
                        .then(pl.lit(0))
                        .otherwise(pl.col("D999RAW"))
                        .alias("D999")
                    ]
                )
                # clean columns, unnest totals
                cases = cases.with_columns(
                    pl.col("RE_Phone")
                    .str.replace_all(r"[^0-9]|2050000000", "")
                    .alias("CLEAN_Phone"),
                    pl.concat_str([pl.col("Address1"), pl.lit(" "), pl.col("Address2")])
                    .str.replace_all(
                        r"JID: \w{3} Hardship.*|Defendant Information.*", ""
                    )
                    .str.strip()
                    .alias("StreetAddress"),
                    pl.col("Name"),
                    pl.col("TOTALS")
                    .list.get(0)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtDue"),
                    pl.col("TOTALS")
                    .list.get(1)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtPaid"),
                    pl.col("TOTALS")
                    .list.get(2)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalBalance"),
                    pl.col("TOTALS")
                    .list.get(3)
                    .str.replace_all(r"[^0-9\.]", "")
                    .cast(pl.Float64, strict=False)
                    .alias("TotalAmtHold"),
                )
                cases = cases.with_columns(
                    pl.when(pl.col("CLEAN_Phone").str.n_chars() < 7)
                    .then(None)
                    .otherwise(pl.col("CLEAN_Phone"))
                    .alias("Phone"),
                )
                cases = cases.with_columns(
                    pl.when(pl.col("HasFeeSheet").is_not())
                    .then(pl.lit(None))
                    .otherwise(pl.col("D999"))
                    .alias("D999")
                )
                cases = cases.fill_null("")
                if not debug:
                    cases = cases.select(
                        "Retrieved",
                        "CaseNumber",
                        "Name",
                        "Alias",
                        "Alias2",
                        "DOB",
                        "Race",
                        "Sex",
                        "TotalAmtDue",
                        "TotalAmtPaid",
                        "TotalBalance",
                        "TotalAmtHold",
                        "D999",
                        "BondAmount",
                        "Phone",
                        "StreetAddress",
                        "City",
                        "State",
                        "ZipCode",
                        "County",
                        "Country",
                        "SSN",
                        "Weight",
                        "Height",
                        "Eyes",
                        "Hair",
                        "FilingDate",
                        "CaseInitiationDate",
                        "ArrestDate",
                        "SuspensionDate",
                        "Speed",
                        "CompletionDate",
                        "OffenseDate",
                        "IndictmentDate",
                        "YouthfulDate",
                        "ALInstitutionalServiceNum",
                        "JuryDemand",
                        "GrandJuryCourtAction",
                        "InpatientTreatmentOrdered",
                        "TrialType",
                        "Judge",
                        "DefendantStatus",
                        "RelatedCases",
                        "ArrestingAgencyType",
                        "CityCodeName",
                        "ArrestingOfficer",
                        "ClearDate",
                        "SpeedLimit",
                        "BloodAlcoholContent",
                        "TicketNumber",
                        "Rule20",
                        "CollectionStatus",
                        "GrandJury",
                        "ProbationOffice#",
                        "ProbationOfficeName",
                        "TrafficCitation#",
                        "DLDestroyDate",
                        "PreviousDUIConvictions",
                        "VehicleDesc",
                        "VehicleState",
                        "DriverLicenseClass",
                        "CommercialVehicle",
                        "TagNumber",
                        "VehicleYear",
                        "PassengersPresent",
                        "CommercialDriverLicenseRequired",
                        "HazardousMaterials",
                        "CaseInitiationType",
                        "DomesticViolence",
                        "AgencyORI",
                        "WarrantIssuanceDate",
                        "WarrantActionDate",
                        "WarrantLocationDate",
                        "WarrantIssuanceStatus",
                        "WarrantActionStatus",
                        "WarrantLocationStatus",
                        "WarrantIssuanceDescription",
                        "WarrantActionDescription",
                        "WarrantLocationDescription",
                        "NumberOfWarrants",
                        "BondType",
                        "BondTypeDesc",
                        "BondCompany",
                        "SuretyCode",
                        "BondReleaseDate",
                        "FailedToAppearDate",
                        "BondsmanProcessIssuance",
                        "BondsmanProcessReturn",
                        "AppealDate",
                        "AppealCourt",
                        "LowerCourtAppealDate",
                        "OriginOfAppeal",
                        "AppealToDesc",
                        "AppealStatus",
                        "AppealTo",
                        "DispositionDateOfAppeal",
                        "DispositionTypeOfAppeal",
                        "NumberOfSubpoenas",
                        "AdminUpdatedBy",
                        "AdminLastUpdate",
                        "TransferToAdminDocDate",
                        "TransferDesc",
                        "TransferReason",
                        "TBNV1",
                        "TBNV2",
                        "DriverLicenseNo",
                        "StateID",
                        "TurnOverDate",
                        "TurnOverAmt",
                        "FrequencyAmt",
                        "DueDate",
                        "OverUnderPaid",
                        "LastPaidDate",
                        "Payor",
                        "EnforcementStatus",
                        "Frequency",
                        "PlacementStatus",
                        "PreTrial",
                        "PreTrialDate",
                        "PreTrialTerms",
                        "PreTermsDate",
                        "Delinquent",
                        "DelinquentDate",
                        "DAMailer",
                        "DAMailerDate",
                        "WarrantMailer",
                        "WarrantMailerDate",
                        "EnforcementLastUpdate",
                        "EnforcementUpdatedBy",
                        "EnforcementComments",
                        "AppealCaseNumber",
                        "ContinuanceDate",
                        "ContinuanceReason",
                        "ContinuanceDescription",
                        "NumberOfPreviousContinuances",
                    )
            self._cases = cases
            return self._cases

    def fees(self, debug=False):
        """
        Make fee sheets table.
        """
        if debug:
            self._fees = None
        # if previously called with debug=True, reset
        if isinstance(self._fees, pl.DataFrame):
            if "FeeSheet" in self._fees.columns:
                self._fees = None
        if isinstance(self._fees, pl.DataFrame):
            return self._fees
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing fee sheets…"):
                df = self.archive.select("CaseNumber", "AllPagesText")
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                        .str.replace(
                            r"\s*\n\s*Admin Fee Balance Garnish Party Amount Due Fee Code Payor Amount Paid",
                            "",
                        )
                        .str.replace(r"^\s*\n", "")
                        .str.replace(
                            "Fee Status Amount Hold Payee Admin Fee Balance Garnish Party Amount Due Fee Code Payor Amount Paid",
                            "",
                        )
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace_all(r"\.\s*\n\s*", ".")
                        .str.strip()
                        .str.split("\n")
                        .alias("FeeSheet"),
                    ]
                )
                df = df.explode("FeeSheet")
                df = df.with_columns(pl.col("FeeSheet").str.strip())
                # non-total rows
                df = df.with_columns(
                    [
                        pl.col("FeeSheet")
                        .str.extract(r"^(I?N?ACTIVE|Total:)")
                        .alias("FeeStatus"),
                        pl.col("FeeSheet")
                        .str.extract(r"^(I?N?ACTIVE)?\s*([YN])", group_index=2)
                        .alias("AdminFee"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"^(I?N?ACTIVE)?\s*([YN])?[\$\d\.,\s]+([A-Z0-9]{4})",
                            group_index=3,
                        )
                        .alias("FeeCode"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"([A-Z0-9]{4}) \$[\d,]+\.\d\d (I?N?ACTIVE)?\s*[YN]?\s",
                            group_index=1,
                        )
                        .alias("Payor"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"([A-Z0-9]{4})\s*([A-Z0-9]+)\s*([A-Z0-9]{4}) \$[\d,]+\.\d\d (I?N?ACTIVE)?\s*[YN]?\s",
                            group_index=2,
                        )
                        .alias("Payee"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"^(I?N?ACTIVE)?\s*([YN]?) \$([\d,]+\.\d\d)", group_index=3
                        )
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("AmountDue"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"^(I?N?ACTIVE)?\s*([YN]?) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d)",
                            group_index=4,
                        )
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("AmountPaid"),
                        pl.col("FeeSheet")
                        .str.extract(r"\$([\d,]+\.\d\d)$")
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("Balance"),
                        pl.col("FeeSheet")
                        .str.extract(
                            r"^(I?N?ACTIVE)?\s*([YN]?) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d)",
                            group_index=5,
                        )
                        .str.replace(",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("AmountHold"),
                    ]
                )
                # total rows
                df = df.with_columns(
                    [
                        pl.when(pl.col("FeeStatus") == "Total:")
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(r"\$([\d,]+\.\d\d)")
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountDue"))
                        .alias("AmountDue"),
                        pl.when(pl.col("FeeStatus") == "Total:")
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"\$([\d,]+\.\d\d) \$([\d,]+\.\d\d)", group_index=2
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountPaid"))
                        .alias("AmountPaid"),
                        pl.when(pl.col("FeeStatus") == "Total:")
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"\$([\d,]+\.\d\d) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d)",
                                group_index=3,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("Balance"))
                        .alias("Balance"),
                        pl.when(pl.col("FeeStatus") == "Total:")
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"\$([\d,]+\.\d\d) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d) \$([\d,]+\.\d\d)",
                                group_index=4,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountHold"))
                        .alias("AmountHold"),
                    ]
                )
                # total rows shift blank amount due
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("FeeSheet").str.contains(
                                r"Total:\s*\$\d+\.\d\d\s*\$\d+\.\d\d\s*\$\d+\.\d\d$"
                            )
                        )
                        .then(None)
                        .otherwise(pl.col("AmountDue"))
                        .alias("AmountDue"),
                        pl.when(
                            pl.col("FeeSheet").str.contains(
                                r"Total:\s*\$\d+\.\d\d\s*\$\d+\.\d\d\s*\$\d+\.\d\d$"
                            )
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"Total:\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)$",
                                group_index=1,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountPaid"))
                        .alias("AmountPaid"),
                        pl.when(
                            pl.col("FeeSheet").str.contains(
                                r"Total:\s*\$\d+\.\d\d\s*\$\d+\.\d\d\s*\$\d+\.\d\d$"
                            )
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"Total:\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)$",
                                group_index=2,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("Balance"))
                        .alias("Balance"),
                        pl.when(
                            pl.col("FeeSheet").str.contains(
                                r"Total:\s*\$\d+\.\d\d\s*\$\d+\.\d\d\s*\$\d+\.\d\d$"
                            )
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"Total:\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)$",
                                group_index=3,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountHold"))
                        .alias("AmountHold"),
                    ]
                )
                # add total column
                df = df.with_columns(
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(pl.lit("Total:"))
                    .otherwise(None)
                    .alias("Total")
                )
                df = df.with_columns(
                    pl.when(pl.col("FeeStatus") == "Total:")
                    .then(None)
                    .otherwise(pl.col("FeeStatus"))
                    .alias("FeeStatus")
                )
                # if no admin fee and no fee status
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("AdminFee").is_null()
                            & pl.col("FeeStatus").is_null()
                            & pl.col("Total").is_null()
                        )
                        .then(
                            pl.col("FeeSheet").str.extract(
                                r"[A-Z0-9]{4} ([A-Z0-9]{4})", group_index=1
                            )
                        )
                        .otherwise(pl.col("Payor"))
                        .alias("Payor"),
                        pl.when(
                            pl.col("AdminFee").is_null()
                            & pl.col("FeeStatus").is_null()
                            & pl.col("Total").is_null()
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(r"\$(\d+\.\d\d)")
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountDue"))
                        .alias("AmountDue"),
                        pl.when(
                            pl.col("AdminFee").is_null()
                            & pl.col("FeeStatus").is_null()
                            & pl.col("Total").is_null()
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"\$(\d+\.\d\d)\s*\$(\d+\.\d\d)", group_index=2
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountPaid"))
                        .alias("AmountPaid"),
                        pl.when(
                            pl.col("AdminFee").is_null()
                            & pl.col("FeeStatus").is_null()
                            & pl.col("Total").is_null()
                        )
                        .then(
                            pl.col("FeeSheet")
                            .str.extract(
                                r"\$(\d+\.\d\d)\s*\$(\d+\.\d\d)\s*\$(\d+\.\d\d)",
                                group_index=3,
                            )
                            .str.replace(",", "")
                            .cast(pl.Float64, strict=False)
                        )
                        .otherwise(pl.col("AmountHold"))
                        .alias("AmountHold"),
                    ]
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Total",
                        "FeeStatus",
                        "AdminFee",
                        "FeeCode",
                        "Payor",
                        "Payee",
                        "AmountDue",
                        "AmountPaid",
                        "Balance",
                        "AmountHold",
                    )
                df = df.filter(pl.col("Balance").is_null().is_not())
            self._fees = df
            return self._fees

    def filing_charges(self, debug=False):
        """
        Make filing charges table.
        """
        if debug:
            self._filing_charges = None
        # if previously called with debug=True, reset
        if isinstance(self._filing_charges, pl.DataFrame):
            if "FilingCharges" in self._filing_charges.columns:
                self._filing_charges = None
        if isinstance(self._filing_charges, pl.DataFrame):
            return self._filing_charges
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing filing charges…"):
                df = self.archive.select("CaseNumber", "AllPagesText")
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Filing Charges(.+?)Disposition Charges")
                        .str.replace(
                            r"\n\s*# Code Description Cite Type Description Category ID Class\s*\n\s*",
                            "",
                        )
                        .str.replace_all(
                            r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", ""
                        )
                        .str.strip()
                        .alias("FilingCharges"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                            group_index=1,
                        )
                        .str.replace("Case Number:", "", literal=True)
                        .str.replace(r"C$", "")
                        .str.strip()
                        .alias("Name"),
                    ]
                )
                df = df.with_columns(
                    pl.col("FilingCharges").apply(
                        lambda x: re.split(
                            r"(?m)(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s*$",
                            x,
                        )
                    )
                )
                df = df.with_columns(
                    [
                        pl.col("FilingCharges")
                        .apply(lambda x: x[0::2][0:-1])
                        .alias("Charge"),
                        pl.col("FilingCharges")
                        .apply(lambda x: x[1::2])
                        .alias("Category"),
                    ]
                )
                df = df.explode("Charge", "Category")
                df = df.with_columns(
                    pl.col("Charge").str.replace_all("\n", "").str.strip()
                )
                df = df.with_columns(
                    [
                        pl.col("Charge").str.extract(r"(\d+)").alias("#"),
                        pl.col("Charge").str.extract(r"\d+ ([A-Z0-9/]+)").alias("Code"),
                        pl.col("Charge")
                        .str.extract(
                            r"\d+ [A-Z0-9/]+ (.+?) [A-Z0-9]{3}-[A-Z0-9]{3}- *[A-Z0-9]{1,3}"
                        )
                        .str.replace(r"([\s-]+)$", "")
                        .str.strip()
                        .alias("Description"),
                        pl.col("Charge")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}- *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?)"
                        )
                        .str.replace_all(" ", "")
                        .str.replace(r"[A-Z]+$", "")
                        .alias("Cite"),
                        pl.col("Charge")
                        .str.extract(
                            r"(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)$"
                        )
                        .alias("TypeDescription"),
                    ]
                )
                df = df.drop_nulls("Charge")
                df = df.with_columns(
                    [
                        pl.when(pl.col("Description").is_null())
                        .then(
                            pl.col("Charge").str.extract(
                                r"\d+ [A-Z0-9]+ (.+?) (BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)$",
                                group_index=1,
                            )
                        )
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # replace stray \ with escape \\
                df = df.with_columns(pl.col("Description").str.replace(r"\\", "\\\\"))
                # fix CFR cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Description").str.contains(r"\d+ CFR \d+")
                    )
                    .then(
                        pl.col("Description")
                        .str.extract(r"(\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?)")
                        .str.replace(r"\. ", ".")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Description").str.contains(r"\d+ CFR \d+")
                    )
                    .then(
                        pl.col("Description").str.replace(
                            r"\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?", ""
                        )
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix ACT XXXX-XX cite
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(ACT \d+-\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix PSC-.+ cite
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(PSC-\d[^\s]+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix SCR-\d+ cite
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(SCR-\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix 760-\d+ cite
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description")
                        .str.extract(r"((DPS)? 760-X-.+)")
                        .str.replace("- ", "-")
                        .str.strip()
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix XXX-XXX$ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(\d+-\d[^\s]+$)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix RULE 32 cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(pl.col("Description").str.contains("RULE 32"))
                        .then(pl.lit("RULE 32"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Description").str.contains("RULE 32"))
                        .then(pl.lit("RULE 32-FELONY"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix PROBATION REV cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(pl.col("Description").str.contains("PROBATION REV"))
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(pl.col("Description").str.contains("PROBATION REV"))
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix COMMUNITY CORRECTION cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").str.contains(
                                "COMMUNITY CORRECTION REVOC"
                            )
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Description").str.contains(
                                "COMMUNITY CORRECTION REVOC"
                            )
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REVOC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix OTHER NON MOVING VIO cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").str.contains("OTHER NON MOVING VIO")
                        )
                        .then(pl.lit("OTHER NON MOVING VIO"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix MC cites at end of description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description")
                        .str.extract(r"(\d+\s*-\s*\d+\s*-\s*\d+$)")
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description")
                        .str.replace(r"(\d+\s*-\s*\d+\s*-\s*\d+$)", "")
                        .str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix 000.000 cites at end of description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(\d+\.\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description").str.replace(r"(\d+\.\d+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix PRE-CONV HABEAS CORPUS cites and descriptions
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").str.contains("PRE-CONV HABEAS CORPUS")
                    )
                    .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(
                        pl.col("Description").str.contains("PRE-CONV HABEAS CORPUS")
                    )
                    .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix HABEAS CORPUS cites and descriptions
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").str.contains("HABEAS CORPUS")
                        & pl.col("Description").str.contains("PRE-CONV").is_not()
                    )
                    .then(pl.lit("HABEAS CORPUS"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(
                        pl.col("Description").str.contains("HABEAS CORPUS")
                        & pl.col("Description").str.contains("PRE-CONV").is_not()
                    )
                    .then(pl.lit("HABEAS CORPUS"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix TRAFFIC/MISC missing description
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Charge").str.contains("TRAFFIC/MISC")
                    )
                    .then(pl.lit("TRAFFIC/MISC"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix BOND FORF
                df = df.with_columns(
                    pl.when(pl.col("Charge").str.contains("BOND FORF-MISD"))
                    .then(pl.lit("BOND FORF-MISD"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(pl.col("Charge").str.contains("BOND FORF-MISD"))
                    .then(pl.lit("BOND FORT"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix MUN- cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(" MUN-")
                    )
                    .then(
                        pl.col("Charge")
                        .str.extract(r"(MUN-.+?) MISDEMEANOR$")
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(" MUN-")
                    )
                    .then(pl.col("Description").str.replace(r"MUN-.+", "").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix MUN-ICI-
                df = df.with_columns(
                    pl.when(pl.col("Cite") == "MUN-ICI-")
                    .then(pl.lit("MUN-ICI-PAL"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix HSV- cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(" HSV-")
                    )
                    .then(
                        pl.col("Charge")
                        .str.extract(
                            r"(HSV-.+?) (MISDEMEANOR|VIOLATION)$", group_index=1
                        )
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(" HSV-")
                    )
                    .then(
                        pl.col("Description").str.replace(r"(HSV-.+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix ORD-AM cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains("ORD-AM")
                    )
                    .then(
                        pl.col("Charge").str.extract(
                            r"(ORD-AM.+?) (MISDEMEANOR|VIOLATION)"
                        )
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains("ORD-AM")
                    )
                    .then(
                        pl.col("Description").str.replace(r"(ORD-AM.+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix missing description when cite is ---------
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Charge").str.contains("----")
                    )
                    .then(pl.col("Charge").str.extract(r"---- (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix MUNICIPAL ORDINANCE extra stuff in description
                df = df.with_columns(
                    pl.when(pl.col("Description").str.contains("MUNICIPAL ORDINANCE"))
                    .then(pl.lit("MUNICIPAL ORDINANCE"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix MUNICIPAL cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains("MUNICIPAL")
                    )
                    .then(pl.col("Charge").str.extract(r"(MUNICIPAL)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix ACT\d+-\d+, SEC \d cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(r"ACT\d+")
                    )
                    .then(pl.col("Charge").str.extract(r"(ACT\d+-\d+, SEC \d)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix PSC cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Charge").str.contains(r" PSC ")
                    )
                    .then(pl.col("Charge").str.extract(r" (PSC) "))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix RESERVED cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Charge").str.contains("RESERVED")
                        & pl.col("Cite").is_null()
                    )
                    .then(pl.lit("RESERVED"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Charge").str.contains("RESERVED")
                        & pl.col("Description").is_null()
                    )
                    .then(pl.col("Charge").str.extract(r"RESERVED (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # remove extra stuff from description
                df = df.with_columns(
                    pl.col("Description")
                    .str.replace(r"-+ +-+", "")
                    .str.replace(r"ADJUDICATIO +N", "")
                    .str.replace(r"(ACT \d+-\d+)", "")
                    .str.replace(r"(PSC-\d[^\s]+)", "")
                    .str.replace(r"(SCR-\d+)", "")
                    .str.replace(r"((DPS)? 760-X-.+)", "")
                    .str.replace(r"(\d+-\d[^\s]+$)", "")
                    .str.replace(r"^, FELONY SEC \d+", "")
                    .str.strip()
                )
                df = df.with_columns(
                    [
                        pl.col("Description").str.extract(r"^([ASCP]) ").alias("ID"),
                        pl.col("Description")
                        .str.replace(r"^([ASCP]) ", "")
                        .alias("Description"),
                    ]
                )
                df = df.with_columns(
                    [
                        pl.col("Charge").str.contains("FELONY").alias("Felony"),
                        (
                            pl.col("Description").str.contains(
                                r"(A ATT|ATT-|ATTEMPT|S SOLICIT|CONSP|SOLICITATION|COMPLICITY|CONSPIRACY|SOLICIT[^I]*[^O]*[^N]*)"
                            )
                            & pl.col("Description").str.contains(r"COMPUTER").is_not()
                        ).alias("ASCNonDisqualifying"),
                        (
                            pl.col("Code").str.contains(
                                r"(OSUA|EGUA|MAN1|MAN2|MANS|ASS1|ASS2|KID1|KID2|HUT1|HUT2|BUR1|BUR2|TOP1|TOP2|TP2D|TP2G|TPCS|TPCD|TPC1|TET2|TOD2|ROB1|ROB2|ROB3|FOR1|FOR2|FR2D|MIOB|TRAK|TRAG|VDRU|VDRY|TRAO|TRFT|TRMA|TROP|CHAB|WABC|ACHA|ACAL|TER1|TFT2|TLP1|TLP2|BIGA|BAC1|ACBL)"
                            )
                            | pl.col("Cite").str.contains(
                                r"026-015-003$|008-016-017|13A-008-0?0?2\.1|13A-008-0?10\.4|13A-010-15[34]|13A-010-171|13A-010-19[45]|13A-010-196\(C\)|13A-010-19[789]|13A-010-200"
                            )
                        ).alias("CERVCode"),
                        (
                            pl.col("Code").str.contains(
                                r"(RAP1|RAP2|SOD1|SOD2|STSA|SXA1|SXA2|ECHI|SX12|CSSC|FTCS|MURD|MRDI|MURR|FMUR|PMIO|POBM|MIPR|POMA|INCE|SX2F|CSSC|ESOC|TMCS|PSMF)"
                            )
                            | pl.col("Cite").str.contains(
                                r"13A-006-066|13A-006-067|13A-006-069\.?1?|13A-006-12[1-5]|13A-012-19[267]|13A-012-200\.2|13A-013-003"
                            )
                        ).alias("PardonCode"),
                        pl.col("Code")
                        .str.contains(r"(CM\d\d|CMUR|OLDD)")
                        .alias("PermanentCode"),
                    ]
                )
                # include all drug trafficking charges based on cite
                df = df.with_columns(
                    pl.when(
                        pl.col("Code").str.contains(r"^TR")
                        & pl.col("Cite").str.contains(r"13A-012-231")
                    )
                    .then(pl.lit(True))
                    .otherwise(pl.col("CERVCode"))
                    .alias("CERVCode")
                )
                df = df.fill_null("")
                df = df.with_columns(
                    [
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("CERVCharge"),
                        (
                            pl.col("PardonCode")
                            & pl.col("Description").str.contains("CAPITAL").is_not()
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("PardonToVoteCharge"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("PermanentCharge"),
                    ]
                )
                if not debug:
                    df = df.select(
                        "Name",
                        "CaseNumber",
                        "#",
                        "Code",
                        "ID",
                        "Description",
                        "Cite",
                        "TypeDescription",
                        "Category",
                        "Felony",
                        "CERVCharge",
                        "PardonToVoteCharge",
                        "PermanentCharge",
                    )
                df = df.with_columns(
                    pl.concat_str(
                        [
                            pl.col("CaseNumber"),
                            pl.lit(" - "),
                            pl.col("#"),
                            pl.lit(" "),
                            pl.col("Cite"),
                            pl.lit(" "),
                            pl.col("Description"),
                            pl.lit(" "),
                            pl.col("TypeDescription"),
                        ]
                    ).alias("ChargesSummary")
                )
                self._filing_charges = df
            return self._filing_charges

    def disposition_charges(self, debug=False):
        """
        Make disposition charges table.
        """
        if debug:
            self._disposition_charges = None
        # if previously called with debug=True, reset
        if isinstance(self._disposition_charges, pl.DataFrame):
            if "Row" in self._disposition_charges.columns:
                self._disposition_charges = None
        if isinstance(self._disposition_charges, pl.DataFrame):
            return self._disposition_charges
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing disposition charges…"):
                df = self.archive.select("AllPagesText", "CaseNumber")
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Disposition Charges (.+?) (Sentences|Enforcement)"
                        )
                        .str.replace(
                            r"# Code Court Action Category Cite Court Action Date\s*\n\s*",
                            "",
                        )
                        .str.replace(
                            r"Type Description Description Class ID\s*\n\s*", ""
                        )
                        .str.replace_all(
                            r"(..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+)", ""
                        )
                        .str.replace(r"^\s*\n\s*", "")
                        .str.replace(r"\s*\n$", "")
                        .alias("DispositionCharges"),
                        pl.col("AllPagesText")
                        .str.extract(r"(Total:.+\$[^\n]*)")
                        .str.replace_all(r"[^0-9|\.|\s|\$]", "")
                        .str.extract_all(r"\s\$\d+\.\d{2}")
                        .list.get(2)
                        .str.replace_all(r"[^0-9\.]", "")
                        .cast(pl.Float64, strict=False)
                        .alias("TotalBalance"),
                        pl.col("AllPagesText")
                        .str.extract(r"(ACTIVE[^\n]+D999[^\n]+)")
                        .str.extract_all(r"\$\d+\.\d{2}")
                        .list.get(-1)
                        .str.replace(r"[\$\s]", "")
                        .cast(pl.Float64, strict=False)
                        .alias("D999"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{10,100})(Case Number)*",
                            group_index=1,
                        )
                        .str.replace("Case Number:", "", literal=True)
                        .str.replace(r"C$", "")
                        .str.strip()
                        .alias("Name"),
                        pl.col("AllPagesText")
                        .str.contains(r"(?s)Fee Sheet (.+Total:[^\n]+)")
                        .alias("HasFeeSheet"),
                    ]
                )
                df = df.with_columns(
                    pl.col("DispositionCharges").apply(
                        lambda x: re.split(r"(?m)^\s*(\d{3}) ", x)
                    )
                )
                df = df.select(
                    pl.col("Name"),
                    pl.col("CaseNumber"),
                    pl.col("DispositionCharges")
                    .apply(lambda x: x[0::2][1:])
                    .alias("Row"),
                    pl.col("DispositionCharges").apply(lambda x: x[1::2]).alias("#"),
                    pl.col("TotalBalance"),
                    pl.col("D999"),
                    pl.col("HasFeeSheet"),
                )
                df = df.explode("Row", "#")
                df = df.with_columns(
                    pl.col("Row").str.replace_all("\n", " ").str.strip()
                )
                df = df.with_columns(
                    [
                        pl.col("Row").str.extract(r"([A-Z0-9/]+)").alias("Code"),
                        pl.col("Row")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("CourtActionDate"),
                        pl.col("Row")
                        .str.extract(
                            r"(BOUND|GUILTY PLEA|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|DISMISSED|FORFEITURE|TRANSFERRE|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|ANCTION|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)"
                        )
                        .str.replace(r" \)", ")")
                        .str.replace(r"\d\d?/\d\d?/\d\d\d\d ", "")
                        .str.replace(
                            r"N OL PROS W/CONDITION S", "NOL PROS W/CONDITIONS"
                        )
                        .str.replace("INSAN E", "INSANE")
                        .str.replace("CONDITION S", "CONDITIONS")
                        .str.replace("PROBATION/S", "PROBATION/SANCTION")
                        .str.replace("ADJUDICATIO N", "ADJUDICATION")
                        .str.replace("TRANSFERRE", "TRANSFERRED")
                        .str.replace("BOUND", "BOUND OVER GJ")
                        .str.replace("DOCKETED", "DOCKETED BY MISTAKE")
                        .alias("CourtAction"),
                        pl.col("Row")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}- *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\d?/?\d?)"
                        )
                        .str.replace_all(" ", "")
                        .str.replace(r"[A-Z/]+$", "")
                        .alias("Cite"),
                        pl.col("Row")
                        .str.extract(
                            r"([A-Z0-9]{3}-[A-Z0-9]{3}- *[A-Z0-9]{1,3}\.?\s*\d*\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\(?[A-Z0-9]*\)?\d?/?\d?.+)"
                        )
                        .str.replace(r"^[A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+", "")
                        .str.replace(r"\d\(.\)\(?.?\)?", "")
                        .str.replace(
                            r"^(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION)",
                            "",
                        )
                        .str.strip()
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(
                            r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|DISMISSED|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|FORFEITURE|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)\s+(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s+(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)",
                            group_index=4,
                        )
                        .str.strip()
                        .alias("DescriptionFirstLine"),
                        pl.col("Row")
                        .str.extract(
                            r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s*(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)",
                            group_index=2,
                        )
                        .alias("TypeDescription"),
                        pl.col("Row")
                        .str.extract(
                            r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)"
                        )
                        .alias("Category"),
                    ]
                )
                # fix DescriptionFirstLine when another field is missing
                df = df.with_columns(
                    pl.when(pl.col("DescriptionFirstLine").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(
                            r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|DISMISSED|FORFEITURE|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)\s+(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s+(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)",
                            group_index=3,
                        )
                        .str.strip()
                    )
                    .otherwise(pl.col("DescriptionFirstLine"))
                    .alias("DescriptionFirstLine")
                )
                df = df.with_columns(
                    pl.when(pl.col("DescriptionFirstLine").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(
                            r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|GJ|GUILTY PLEA|NOT GUILTY/INSAN E|WAIVED TO GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|DISMISSED|FORFEITURE|TRANSFER|REMANDED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|ANCTION|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)\s+(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)",
                            group_index=3,
                        )
                        .str.strip()
                    )
                    .otherwise(pl.col("DescriptionFirstLine"))
                    .alias("DescriptionFirstLine")
                )
                df = df.with_columns(
                    pl.when(pl.col("DescriptionFirstLine").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(
                            r"(ALCOHOL|BOND FORFEITURE|CONSERVATION|DOCKET/MISC|DRUG|GOVERNMENT PUBLIC|HEALTH|MUNICIPAL ORDINANCE|MUNICIPAL|OTHER|PERSONAL|PROPERTY|SEX OFFENSE|TRAFFIC|DOCKET|REVENUE – PSC \(PUBLIC SERVICE COMMISSION\)|BUSINESS|JUVENILE)\s+(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)",
                            group_index=3,
                        )
                        .str.strip()
                    )
                    .otherwise(pl.col("DescriptionFirstLine"))
                    .alias("DescriptionFirstLine")
                )
                df = df.with_columns(
                    pl.when(pl.col("DescriptionFirstLine").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(
                            r"(WAIVED TO GJ \d\d/\d\d/\d\d\d\d|WAIVED TO GJ|GUILTY PLEA|NOT GUILTY/INSAN E|GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|DISMISSED|FORFEITURE|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|ANCTION|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)\s+(.+?)([A-Z0-9]{3}-\s*[A-Z0-9]{3}-\s*[^\s]+)",
                            group_index=2,
                        )
                        .str.strip()
                    )
                    .otherwise(pl.col("DescriptionFirstLine"))
                    .alias("DescriptionFirstLine")
                )
                # clean DescriptionFirstLine
                df = df.with_columns(
                    pl.when(
                        pl.col("DescriptionFirstLine").is_in(
                            [
                                "CONSERVATION",
                                "TO GJ",
                                "PROPERTY",
                                "DRUG",
                                "PERSONAL",
                                "FELONY",
                                "ANCTION    DRUG",
                                "MISDEMEANOR",
                            ]
                        )
                        | pl.col("DescriptionFirstLine").str.contains(
                            r"\d\d/\d\d/\d\d\d\d"
                        )
                    )
                    .then(pl.lit(None))
                    .otherwise(pl.col("DescriptionFirstLine"))
                    .alias("DescriptionFirstLine")
                )
                # if description is in two lines, concat
                df = df.with_columns(
                    pl.when(pl.col("DescriptionFirstLine").is_null().is_not())
                    .then(
                        pl.concat_str(
                            [
                                pl.col("DescriptionFirstLine"),
                                pl.lit(" "),
                                pl.col("Description"),
                            ]
                        )
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # replace stray \ with escape \\
                # remove TypeDescription at beginning of desc
                # remove (PUBLIC SERVICE COMMISSION)
                df = df.with_columns(
                    pl.col("Description")
                    .str.replace(r"\\", "\\\\")
                    .str.replace(
                        r"^(BOND|FELONY|MISDEMEANOR|OTHER|TRAFFIC|VIOLATION|\(PUBLIC SERVICE COMMISSION\))",
                        "",
                    )
                    .str.strip()
                )
                # fix CFR cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains(r"\d+ CFR \d+")
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(r"(\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)?)")
                        .str.replace(r"\. ", ".")
                        .str.strip()
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains(r"\d+ CFR \d+")
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(r"\d+ CFR \d+\.\s*\d+\(?.?\)?\(?.?\)? (.+)")
                        .str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix ACT XXXX-XX cite, description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(ACT \d+-\d+)").str.strip())
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains(r"(ACT \d+-\d+)")
                    )
                    .then(pl.col("Row").str.extract(r"ACT \d+-\d+ (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix PSC-.+ cite, description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description").str.extract(r"(PSC-\d[^\s]+)").str.strip()
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains(r"(PSC-\d[^\s]+)")
                    )
                    .then(pl.col("Row").str.extract(r"PSC-\d[^\s]+ (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix SCR-\d+ cite
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(SCR-\d+)").str.strip())
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains(r"(SCR-\d+)")
                    )
                    .then(pl.col("Row").str.extract(r"SCR-\d+ (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix 760-\d+ cite
                df = df.with_columns(
                    pl.when(pl.col("Row").str.contains(r"(760-X-)"))
                    .then(
                        pl.col("Row")
                        .str.extract(r"((DPS)? 760-X- ?[^\s]+)")
                        .str.replace("- ", "-")
                        .str.replace_all(" ", "")
                        .str.strip()
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(pl.col("Row").str.contains(r"(760-X-)"))
                    .then(pl.col("Row").str.extract(r"760-X-[^\s]+(.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix XXX-XXX$ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(\d+-\d[^\s]+$)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix ORD- \d+-\d+ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(ORD- \d+-\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix HSV- OR-D \d+-\d+ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(HSV- OR-D \d+-\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix \d\d\d-\d\d\d([A-Z0-9]) cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(\d+-\d+\([A-Z0-9]\))"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix PSC-\d\.\d-\d+ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(PSC-\d+\.\d+-\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix \d+-\d+ -\d+ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(r"(\d+-\d+ -\d+)")
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix \d+\.\d+ cites
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Row").str.extract(r"(\d+\.\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix MUNICIPAL cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null()
                        & pl.col("Row").str.contains("MUNICIPAL MUNICIPAL")
                    )
                    .then(pl.col("Row").str.extract(r"(MUNICIPAL)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # fix RULE 32 cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").str.contains("RULE 32")
                            | (
                                pl.col("Row").str.contains("RULE 32")
                                & pl.col("Description").is_null()
                            )
                        )
                        .then(pl.lit("RULE 32"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Description").str.contains("RULE 32")
                            | (
                                pl.col("Row").str.contains("RULE 32")
                                & pl.col("Description").is_null()
                            )
                        )
                        .then(pl.lit("RULE 32-FELONY"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix PROBATION REV cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Row").str.contains("PROBATION REV")
                            & (pl.col("Cite").is_null() | pl.col("Cite").eq(""))
                        )
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Row").str.contains("PROBATION REV")
                            & (
                                pl.col("Description").is_null()
                                | pl.col("Description").eq("")
                            )
                        )
                        .then(pl.lit("PROBATION REV"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix COMMUNITY CORRECTION cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Row").str.contains("COMMUNITY CORRECTION REVOC")
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REV"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                        pl.when(
                            pl.col("Row").str.contains("COMMUNITY CORRECTION REVOC")
                        )
                        .then(pl.lit("COMMUNITY CORRECTION REVOC"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                    ]
                )
                # fix OTHER NON MOVING VIO cites and descriptions
                df = df.with_columns(
                    [
                        pl.when(pl.col("Row").str.contains("OTHER NON MOVING VIO"))
                        .then(pl.lit("OTHER NON MOVING VIO"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix MC cites at end of description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description")
                        .str.extract(r"(\d+\s*-\s*\d+\s*-\s*\d+$)")
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description")
                        .str.replace(r"(\d+\s*-\s*\d+\s*-\s*\d+$)", "")
                        .str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix 000.000 cites at end of description
                df = df.with_columns(
                    pl.when(pl.col("Cite").is_null())
                    .then(pl.col("Description").str.extract(r"(\d+\.\d+)"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(pl.col("Cite").is_null())
                    .then(
                        pl.col("Description").str.replace(r"(\d+\.\d+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix PRE-CONV HABEAS CORPUS cites and descriptions
                df = df.with_columns(
                    pl.when(pl.col("Row").str.contains("PRE-CONV HABEAS CORPUS"))
                    .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(pl.col("Row").str.contains("PRE-CONV HABEAS CORPUS"))
                    .then(pl.lit("PRE-CONV HABEAS CORPUS"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix HABEAS CORPUS cites and descriptions
                df = df.with_columns(
                    pl.when(
                        pl.col("Row").str.contains("HABEAS CORPUS")
                        & pl.col("Row").str.contains("PRE-CONV").is_not()
                    )
                    .then(pl.lit("HABEAS CORPUS"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(
                        pl.col("Row").str.contains("HABEAS CORPUS")
                        & pl.col("Row").str.contains("PRE-CONV").is_not()
                    )
                    .then(pl.lit("HABEAS CORPUS"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix TRAFFIC/MISC missing description
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains("TRAFFIC/MISC")
                    )
                    .then(pl.lit("TRAFFIC/MISC"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix MUN- cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains(" MUN-")
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(r"(MUN-.+?) MISDEMEANOR$")
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains(" MUN-")
                    )
                    .then(pl.col("Description").str.replace(r"MUN-.+", "").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix HSV- cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains(" HSV-")
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(
                            r"(HSV-.+?) (MISDEMEANOR|VIOLATION)$", group_index=1
                        )
                        .str.replace_all(" ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains(" HSV-")
                    )
                    .then(
                        pl.col("Description").str.replace(r"(HSV-.+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix ORD-AM cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains("ORD-AM")
                    )
                    .then(
                        pl.col("Row").str.extract(
                            r"(ORD-AM.+?) (MISDEMEANOR|VIOLATION)"
                        )
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Cite").is_null() & pl.col("Row").str.contains("ORD-AM")
                    )
                    .then(
                        pl.col("Description").str.replace(r"(ORD-AM.+)", "").str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix MUNICIPAL ORDINANCE extra stuff in description
                df = df.with_columns(
                    pl.when(pl.col("Description").str.contains("MUNICIPAL ORDINANCE"))
                    .then(pl.lit("MUNICIPAL ORDINANCE"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix BOND FORT missing description, cite
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r"BOND FORT")
                    )
                    .then(pl.lit("BOND FORF-FELONY"))
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r"BOND FORT")
                    )
                    .then(pl.lit("BOND FORT"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix PT-RL F/CN missing description
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r"PT-RL F/CN")
                    )
                    .then(pl.lit("PT-RL F/CN"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix - - (Description) missing
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r" -+ +-+ +")
                    )
                    .then(pl.col("Row").str.extract(r"-+ +-+ +(.+)"))
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix missing description when cite is ---------
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains("----")
                    )
                    .then(pl.col("Row").str.extract(r"---- (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix RESERVED cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Row").str.contains("RESERVED")
                        & pl.col("Cite").is_null()
                    )
                    .then(pl.lit("RESERVED"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Row").str.contains("RESERVED")
                        & pl.col("Description").is_null()
                    )
                    .then(pl.col("Row").str.extract(r"RESERVED (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # fix SECTION \d\d-\d? cites
                df = df.with_columns(
                    pl.when(
                        pl.col("Row").str.contains("SECTION")
                        & pl.col("Description").is_null()
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(r"SECTION \d\d-\d* (.+)")
                        .str.replace(r"^\s*MISDEMEANOR \d+", "")
                        .str.strip()
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                    pl.when(
                        pl.col("Row").str.contains("SECTION") & pl.col("Cite").is_null()
                    )
                    .then(
                        pl.col("Row")
                        .str.extract(r"(SECTION \d+-\s*(MISDEMEANOR)?\s*\d+)")
                        .str.replace(" MISDEMEANOR ", "")
                    )
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                )
                # fix misc -\.?\d+ descriptions
                df = df.with_columns(
                    pl.when(pl.col("Description").is_null())
                    .then(
                        pl.col("Row")
                        .str.extract(r"[-\.]\d+(.+?)$")
                        .str.strip()
                        .str.replace(r"^\([A-Z0-9]\)", "")
                        .str.replace(r"^\([A-Z0-9]\)", "")
                        .str.replace(r"^\.\d+", "")
                    )
                    .otherwise(pl.col("Description"))
                    .alias("Description")
                )
                # fix "PSC" cite and description
                df = df.with_columns(
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r" PSC ")
                    )
                    .then(pl.lit("PSC"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite"),
                    pl.when(
                        pl.col("Description").is_null()
                        & pl.col("Row").str.contains(r" PSC ")
                    )
                    .then(pl.col("Row").str.extract(r" PSC (.+)").str.strip())
                    .otherwise(pl.col("Description"))
                    .alias("Description"),
                )
                # missing TypeDescriptions caused by another missing field
                df = df.with_columns(
                    pl.when(pl.col("TypeDescription").is_null())
                    .then(
                        pl.col("Row").str.extract(
                            r"(BOND|FELONY|MISDEMEANOR|OTHER|VIOLATION|TRAFFIC)"
                        )
                    )
                    .otherwise(pl.col("TypeDescription"))
                    .alias("TypeDescription")
                )
                # fix MISCELLANEOUS FILING
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("MISCELLANEOUS FILING")
                        )
                        .then(pl.lit("MISCELLANEOUS FILING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix SHOW CAUSE DKT/HEARING
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("SHOW CAUSE DKT/HEARING")
                        )
                        .then(pl.lit("SHOW CAUSE DKT/HEARING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix BOND HEARING
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("BOND HEARING")
                        )
                        .then(pl.lit("BOND HEARING"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix MUNICIPAL ORDINANCE
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains(
                                "MUNICIPAL MUNICIPAL ORDINANCE"
                            )
                        )
                        .then(pl.lit("MUNICIPAL ORDINANCE"))
                        .otherwise(pl.col("Description"))
                        .alias("Description")
                    ]
                )
                # fix MUN- OR-D 13-4
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("MUN- OR-D 13-4")
                        )
                        .then(pl.lit("NOISE - LOUD & EXCESS"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("MUN- OR-D 13-4")
                        )
                        .then(pl.lit("MUN- OR-D 13-4"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    ]
                )
                # fix ACT2001-312, SEC 5
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("Description").is_null()
                            & pl.col("Row").str.contains("ACT2001-312")
                        )
                        .then(pl.lit("OBSTRUCT JUSTICE BY FALSE ID"))
                        .otherwise(pl.col("Description"))
                        .alias("Description"),
                        pl.when(
                            pl.col("Cite").is_null()
                            & pl.col("Row").str.contains("ACT2001-312")
                        )
                        .then(pl.lit("ACT2001-312, SEC 5"))
                        .otherwise(pl.col("Cite"))
                        .alias("Cite"),
                    ]
                )
                # fix ugly -- -- from cite in description and hanging N in ADJUDICATIO N
                df = df.with_columns(
                    pl.col("Description")
                    .str.replace(r"-+ +-+", "")
                    .str.replace("ADJUDICATIO N", "")
                    .str.replace(r"\s+N$", "")
                    .str.replace(r"^ORDINANCE (VIOLATION|MISDEMEANOR)\s+", "")
                    .str.replace(r"^, FELONY SEC \d+", "")
                    .str.strip()
                )
                # fix MUN-ICI-
                df = df.with_columns(
                    pl.when(pl.col("Cite").eq("MUN-ICI-"))
                    .then(pl.lit("MUN-ICI-PAL"))
                    .otherwise(pl.col("Cite"))
                    .alias("Cite")
                )
                # remove null rows
                df = df.drop_nulls("Row")
                # add ID column
                df = df.with_columns(
                    pl.col("Row")
                    .str.extract(r"\d\d/\d\d/\d\d\d\d ([ASCP]) ")
                    .alias("ID")
                )
                # remove ID from description
                df = df.with_columns(pl.col("Description").str.replace(r"^\w ", ""))
                ## charge sort
                df = df.with_columns(
                    [
                        pl.col("CourtAction")
                        .str.contains(r"GUILTY|CONVICTED")
                        .alias("Conviction"),
                        pl.col("Row").str.contains("FELONY").alias("Felony"),
                        (
                            pl.col("Description").str.contains(
                                r"(A ATT|ATT-|ATTEMPT|S SOLICIT|CONSP|SOLICITATION|COMPLICITY|CONSPIRACY|SOLICIT[^I]*[^O]*[^N]*)"
                            )
                            & pl.col("Description").str.contains(r"COMPUTER").is_not()
                        ).alias("ASCNonDisqualifying"),
                        (
                            pl.col("Code").str.contains(
                                r"(OSUA|EGUA|MAN1|MAN2|MANS|ASS1|ASS2|KID1|KID2|HUT1|HUT2|BUR1|BUR2|TOP1|TOP2|TP2D|TP2G|TPCS|TPCD|TPC1|TET2|TOD2|ROB1|ROB2|ROB3|FOR1|FOR2|FR2D|MIOB|TRAK|TRAG|VDRU|VDRY|TRAO|TRFT|TRMA|TROP|CHAB|WABC|ACHA|ACAL|TER1|TFT2|TLP1|TLP2|BIGA|BAC1|ACBL)"
                            )
                            | pl.col("Cite").str.contains(
                                r"026-015-003$|008-016-017|13A-008-0?0?2\.1|13A-008-0?10\.4|13A-010-15[34]|13A-010-171|13A-010-19[45]|13A-010-196\(C\)|13A-010-19[789]|13A-010-200"
                            )
                        ).alias("CERVCode"),
                        (
                            pl.col("Code").str.contains(
                                r"(RAP1|RAP2|SOD1|SOD2|STSA|SXA1|SXA2|ECHI|SX12|CSSC|FTCS|MURD|MRDI|MURR|FMUR|PMIO|POBM|MIPR|POMA|INCE|SX2F|CSSC|ESOC|TMCS|PSMF)"
                            )
                            | pl.col("Cite").str.contains(
                                r"13A-006-066|13A-006-067|13A-006-069\.?1?|13A-006-12[1-5]|13A-012-19[267]|13A-012-200\.2|13A-013-003"
                            )
                        ).alias("PardonCode"),
                        (
                            pl.col("Code").str.contains(r"(CM\d\d|CMUR|OLDD)")
                            | pl.col("Description").str.contains("CAPITAL")
                        ).alias("PermanentCode"),
                    ]
                )
                # include all drug trafficking charges based on cite
                df = df.with_columns(
                    pl.when(
                        pl.col("Code").str.contains(r"^TR")
                        & pl.col("Cite").str.contains(r"13A-012-231")
                    )
                    .then(pl.lit(True))
                    .otherwise(pl.col("CERVCode"))
                    .alias("CERVCode")
                )
                df = df.with_columns(
                    pl.when(pl.col("Conviction").is_null())
                    .then(pl.lit(False))
                    .otherwise(pl.col("Conviction"))
                    .alias("Conviction")
                )
                df = df.with_columns(
                    [
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("CERVCharge"),
                        (
                            pl.col("PardonCode")
                            & pl.col("Description").str.contains("CAPITAL").is_not()
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("PardonToVoteCharge"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Felony")
                        ).alias("PermanentCharge"),
                        (
                            pl.col("CERVCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("CERVConviction"),
                        (
                            pl.col("PardonCode")
                            & pl.col("Description").str.contains("CAPITAL").is_not()
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("PardonToVoteConviction"),
                        (
                            pl.col("PermanentCode")
                            & pl.col("ASCNonDisqualifying").is_not()
                            & pl.col("Conviction")
                            & pl.col("Felony")
                        ).alias("PermanentConviction"),
                    ]
                )
                df = df.with_columns(
                    pl.when(pl.col("Conviction").is_not())
                    .then(pl.lit(None))
                    .otherwise(pl.col("CERVConviction"))
                    .alias("CERVConviction"),
                    pl.when(pl.col("Conviction").is_not())
                    .then(pl.lit(None))
                    .otherwise(pl.col("PardonToVoteConviction"))
                    .alias("PardonToVoteConviction"),
                    pl.when(pl.col("Conviction").is_not())
                    .then(pl.lit(None))
                    .otherwise(pl.col("PermanentConviction"))
                    .alias("PermanentConviction"),
                )
                df = df.with_columns(
                    [
                        pl.when(pl.col("D999").is_null())
                        .then(pl.lit(0.0))
                        .otherwise(pl.col("D999"))
                        .alias("D999"),
                        pl.when(pl.col("TotalBalance").is_null())
                        .then(pl.lit(0.0))
                        .otherwise(pl.col("TotalBalance"))
                        .alias("TotalBalance"),
                    ]
                )
                df = df.with_columns(
                    [
                        pl.when(
                            pl.col("CERVConviction")
                            | pl.col("PardonToVoteConviction")
                            | pl.col("PermanentConviction")
                        )
                        .then(pl.col("TotalBalance") - pl.col("D999"))
                        .otherwise(None)
                        .alias("PaymentToRestore")
                    ]
                )
                df = df.with_columns(
                    pl.when(pl.col("HasFeeSheet").is_not())
                    .then(pl.lit(None))
                    .otherwise(pl.col("TotalBalance"))
                    .alias("TotalBalance")
                )
                if not debug:
                    df = df.select(
                        "Name",
                        "CaseNumber",
                        "#",
                        "Code",
                        "ID",
                        "Description",
                        "Cite",
                        "TypeDescription",
                        "Category",
                        "CourtAction",
                        "CourtActionDate",
                        "TotalBalance",
                        "PaymentToRestore",
                        "Conviction",
                        "Felony",
                        "CERVCharge",
                        "PardonToVoteCharge",
                        "PermanentCharge",
                        "CERVConviction",
                        "PardonToVoteConviction",
                        "PermanentConviction",
                    )
                df = df.with_columns(
                    pl.col("CourtActionDate")
                    .dt.to_string("%y-%m-%d")
                    .alias("CourtActionDateStr")
                )
                df = df.fill_null("")
                df = df.with_columns(
                    pl.concat_str(
                        [
                            pl.col("CaseNumber"),
                            pl.lit(" - "),
                            pl.col("#"),
                            pl.lit(" "),
                            pl.col("Cite"),
                            pl.lit(" "),
                            pl.col("Description"),
                            pl.lit(" "),
                            pl.col("TypeDescription"),
                            pl.lit(" "),
                            pl.col("CourtAction"),
                            pl.lit(" "),
                            pl.col("CourtActionDateStr"),
                        ]
                    ).alias("ChargesSummary")
                )
                df = df.drop("CourtActionDateStr")
            self._disposition_charges = df
            return self._disposition_charges

    def sentences(self, debug=False):
        """
        Make sentences table.
        """
        if debug:
            self._sentences = None
        # if previously called with debug=True, reset
        if isinstance(self._sentences, pl.DataFrame):
            if "Sentence" in self._sentences.columns:
                self._sentences = None
        if isinstance(self._sentences, pl.DataFrame):
            return self._sentences
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing sentences…"):
                df = self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract_all(r"(?s)(Sentence \d+ .+? \*Key)")
                    .alias("Sentence"),
                )
                df = df.drop_nulls("Sentence")
                df = df.explode("Sentence")
                df = df.with_columns(
                    pl.col("Sentence").str.replace_all(
                        r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", ""
                    )
                )
                df = df.with_columns(
                    # sentence
                    pl.col("Sentence")
                    .str.extract(r"^Sentence (\d+)")
                    .cast(pl.Int64, strict=False)
                    .alias("Sentence#"),
                    pl.col("Sentence")
                    .str.extract(r"Last Update: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("LastUpdate"),
                    pl.col("Sentence")
                    .str.extract(r"Updated By: (\w+)")
                    .alias("UpdatedBy"),
                    pl.col("Sentence")
                    .str.extract(r"Probation Revoke: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ProbationRevoke"),
                    pl.col("Sentence")
                    .str.extract(
                        r"License Susp Period: (\d+ Years, \d+ Months, \d+ Days\.)"
                    )
                    .alias("LicenseSuspPeriod"),
                    pl.col("Sentence")
                    .str.extract(
                        r"License Susp Period: (\d+ Years, \d+ Months, \d+ Days\.)?\s*\n\s*(\d\d/\d\d/\d\d\d\d)?\s*\n?\s*(\d+ Years, \d+ Months, \d+ Days\.)?",
                        group_index=2,
                    )
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("ProbationBeginDate"),
                    pl.col("Sentence")
                    .str.extract(
                        r"License Susp Period: (\d+ Years, \d+ Months, \d+ Days\.)?\s*\n\s*(\d\d/\d\d/\d\d\d\d)?\s*\n?\s*(\d+ Years, \d+ Months, \d+ Days\.)",
                        group_index=3,
                    )
                    .alias("JailCreditPeriod"),
                    pl.col("Sentence")
                    .str.extract(
                        r"Probation Period: (\d+ Years, \d+ Months, \d+ Days\.)"
                    )
                    .alias("ProbationPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Provisions: (\w+)")
                    .str.replace("Requrements", "")
                    .alias("SentenceProvisions"),
                    pl.col("Sentence")
                    .str.extract(r"Requrements Completed: (YES|NO|UNKNOWN)")
                    .alias("RequirementsCompleted"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceDate"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence Start Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceStartDate"),
                    pl.col("Sentence")
                    .str.extract(r"Sentence End Date: (\d\d/\d\d/\d\d\d\d)")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("SentenceEndDate"),
                    # monetary
                    pl.col("Sentence")
                    .str.extract(r"Costs: (.+?)Fine")
                    .str.strip()
                    .alias("Costs"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)Alias Warrant:.+?\n\s*(\w+)\s*\n\s*Drug Docket Fees"
                    )
                    .alias("DrugUserFee"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"WC Fee 85%: (.+)", group_index=1)
                    .str.strip()
                    .alias("DrugDocketFees"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"Jail Fee: (.+)")
                    .str.strip()
                    .alias("JailFee"),
                    pl.col("Sentence")
                    .str.extract(r"Demand Reduction Hearing: (.+)")
                    .str.strip()
                    .alias("DemandReductionHearing"),
                    pl.col("Sentence")
                    .str.extract(r"Fine Imposed: (.+)")
                    .str.strip()
                    .cast(pl.Float64, strict=False)
                    .alias("FineImposed"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)License Suspension Fee:[^\n]*\n\s*([^\n]+)")
                    .str.extract(r"([\d\.+]+)")
                    .str.strip()
                    .cast(pl.Float64, strict=False)
                    .alias("FineSuspended"),  # don't ask me why
                    pl.col("Sentence")
                    .str.extract(r"(.+) Amt Over Minimum CVF:")
                    .str.strip()
                    .alias("AliasWarrant"),
                    # no perfect way to distinguish Subpoena from AttorneyFees
                    pl.col("Sentence")
                    .str.extract(r"Subpoena:(.+?)Attorney Fees")
                    .str.strip()
                    .str.extract(r"([^\s]+)$")
                    .alias("AttorneyFees"),
                    pl.col("Sentence")
                    .str.extract(r"Subpoena:(.+?)Attorney Fees")
                    .str.strip()
                    .str.extract(r"^([^\s]) ")
                    .alias("Subpoena"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)Drug User Fee:\s*\n(.+?)\s*\n\s*Subpoena:")
                    .str.replace_all(" ", "")
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("PrelimHearing"),
                    pl.col("Sentence")
                    .str.extract(r"Crime History Fee: (.+)")
                    .str.strip()
                    .alias("CrimeHistoryFee"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)License Suspension Fee: ([^\n]+)\n([^\n]+)\n([^\n]+)",
                        group_index=2,
                    )
                    .str.extract(r"([A-Z])")
                    .alias("Fine"),
                    pl.col("Sentence")
                    .str.extract(
                        r"(?s)License Suspension Fee: ([^\n]+)\n([^\n]+)\n([^\n]+)",
                        group_index=3,
                    )
                    .str.replace(r"WC.+", "")
                    .str.strip()
                    .alias("CrimeVictimsFee"),
                    pl.col("Sentence")
                    .str.extract(r"(.+) WC Fee 85%:")
                    .str.strip()
                    .alias("WCFee85%"),
                    pl.col("Sentence")
                    .str.extract(r"SX10: (.+)")
                    .str.strip()
                    .alias("SX10"),
                    # no perfect way to distinguish AmtOverMinimumCVF from RemovalBill
                    pl.col("Sentence")
                    .str.extract(r"Amt Over Minimum CVF:(.+)WC Fee DA:")
                    .str.strip()
                    .str.extract(r"^([^\s]+)")
                    .alias("AmtOverMinimumCVF"),
                    pl.col("Sentence")
                    .str.extract(r"Amt Over Minimum CVF:(.+)WC Fee DA:")
                    .str.strip()
                    .str.extract(r"[^\s]+ (.+)")
                    .alias("RemovalBill"),
                    pl.col("Sentence")
                    .str.extract(r"License Suspension Fee: (.+)")
                    .str.strip()
                    .alias("LicenseSuspensionFee"),
                    pl.col("Sentence")
                    .str.extract(r"Municipal Court: (.+)")
                    .str.strip()
                    .alias("MunicipalCourt"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)WC Fee 85%:\s*\n([^\n]+)")
                    .str.replace(r"Demand.+", "")
                    .str.strip()
                    .alias("WCFeeDA"),
                    pl.col("Sentence")
                    .str.extract(r"Immigration Fine:(.+)")
                    .str.replace(" Fine Imposed.+", "")
                    .str.strip()
                    .alias("ImmigrationFine"),
                    # confinement
                    pl.col("Sentence")
                    .str.extract(
                        r"Imposed Confinement Period: (\d+ Years, \d+ Months, \d+ Days\.)"
                    )
                    .alias("ImposedConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(
                        r"Total Confinement Period: (\d+ Years, \d+ Months, \d+ Days\.)"
                    )
                    .alias("TotalConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(
                        r"Suspended Confinement Period (\d+ Years, \d+ Months, \d+ Days\.)"
                    )
                    .alias("SuspendedConfinementPeriod"),
                    pl.col("Sentence")
                    .str.extract(r"Boot Camp: (.+)")
                    .str.strip()
                    .alias("BootCamp"),
                    pl.col("Sentence")
                    .str.extract(r"Penitentiary: (.+)")
                    .str.strip()
                    .alias("Penitentiary"),
                    pl.col("Sentence")
                    .str.extract(r"Life Without Parole: (.+)")
                    .str.strip()
                    .alias("LifeWithoutParole"),
                    pl.col("Sentence")
                    .str.extract(r"Death: (.+)Life")
                    .str.strip()
                    .alias("Death"),
                    pl.col("Sentence")
                    .str.extract(r"Life: (.+)Jail")
                    .str.strip()
                    .alias("Life"),
                    pl.col("Sentence")
                    .str.extract(r"Jail: (.+)")
                    .str.strip()
                    .alias("Jail"),
                    pl.col("Sentence")
                    .str.extract(r"Electronic Monitoring:(.+)Reverse")
                    .str.strip()
                    .str.extract(r"^([^\s]+)")
                    .alias("ElectronicMonitoring"),
                    pl.col("Sentence")
                    .str.extract(r"Consecutive Sentence:(.+)")
                    .str.strip()
                    .alias("ConsecutiveSentence"),
                    pl.col("Sentence")
                    .str.extract(r"Chain Gang: (.+)")
                    .str.strip()
                    .alias("ChainGang"),
                    pl.col("Sentence")
                    .str.extract(r"Electronic Monitoring:(.+)Reverse")
                    .str.strip()
                    .str.extract(r"^[^\s]+ (.+)")
                    .alias("ReverseSplit"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Coterminous Sentence")
                    .str.strip()
                    .alias("CoterminousSentence"),
                    # programs
                    pl.col("Sentence")
                    .str.extract(r"Jail Diversion:(.+?)Alcoholics")
                    .str.strip()
                    .alias("JailDiversion"),
                    pl.col("Sentence")
                    .str.extract(r"Informal Probation:(.+)")
                    .str.strip()
                    .alias("InformalProbation"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Dui School:")
                    .str.strip()
                    .alias("DocDrugProgram"),
                    pl.col("Sentence")
                    .str.extract(r"Dui School:(.+?)Defensive")
                    .str.strip()
                    .alias("DuiSchool"),
                    pl.col("Sentence")
                    .str.extract(r"Defensive Driving Shcool:(.+)")
                    .str.strip()
                    .alias("DefensiveDrivingSchool"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Community Service:")
                    .str.strip()
                    .cast(pl.Int64, strict=False)
                    .alias("CommunityServiceHrs"),
                    pl.col("Sentence")
                    .str.extract(r"Bad Check School:(.+)")
                    .str.strip()
                    .alias("BadCheckSchool"),
                    pl.col("Sentence")
                    .str.extract(r"Drug Court:(.+)")
                    .str.strip()
                    .alias("CourtReferralProgram"),
                    # enhanced
                    pl.col("Sentence")
                    .str.extract(r"Drug Near Project: (.+?) Drugs")
                    .alias("DrugNearProject"),
                    pl.col("Sentence")
                    .str.extract(r"Habitual Offender: (.+)")
                    .str.strip()
                    .alias("HabitualOffender"),
                    pl.col("Sentence")
                    .str.extract(r"Drug:(.+?)Drug")
                    .str.strip()
                    .alias("Drug"),
                    pl.col("Sentence")
                    .str.extract(r"Sex Offender Community Notification:(.+)")
                    .str.strip()
                    .alias("SexOffenderCommunityNotification"),
                    pl.col("Sentence")
                    .str.extract(r"Drug Code:(.+)")
                    .str.strip()
                    .alias("DrugCode"),
                    pl.col("Sentence")
                    .str.extract(r"Victim DOB: (.+)")
                    .str.strip()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("VictimDOB"),
                    pl.col("Sentence")
                    .str.extract(r"Drugs Near School:(.+)")
                    .str.strip()
                    .alias("DrugsNearSchool"),
                    pl.col("Sentence")
                    .str.extract(r"(.+)Drug Volume:")
                    .str.strip()
                    .cast(pl.Float64, strict=False)
                    .alias("DrugVolume"),
                    pl.col("Sentence")
                    .str.extract(r"(?s)([^\n]+)\n\s*Victim DOB")
                    .str.strip()
                    .alias("DrugMeasureUnit"),
                    pl.col("Sentence")
                    .str.extract(r"(.+) Habitual Offender Number:")
                    .alias("HabitualOffenderNumber"),
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "RequirementsCompleted",
                        "SentenceProvisions",
                        "JailCreditPeriod",
                        "SentenceDate",
                        "SentenceStartDate",
                        "SentenceEndDate",
                        "ProbationPeriod",
                        "ProbationBeginDate",
                        "ProbationRevoke",
                        "LicenseSuspPeriod",
                        "LastUpdate",
                        "UpdatedBy",
                        "Costs",
                        "Fine",
                        "FineImposed",
                        "FineSuspended",
                        "ImmigrationFine",
                        "CrimeVictimsFee",
                        "CrimeHistoryFee",
                        "LicenseSuspensionFee",
                        "DrugUserFee",
                        "WCFee85%",
                        "MunicipalCourt",
                        "JailFee",
                        "DrugDocketFees",
                        "WCFeeDA",
                        "RemovalBill",
                        "AmtOverMinimumCVF",
                        "AliasWarrant",
                        "SX10",
                        "PrelimHearing",
                        "AttorneyFees",
                        "DemandReductionHearing",
                        "Subpoena",
                        "ImposedConfinementPeriod",
                        "SuspendedConfinementPeriod",
                        "TotalConfinementPeriod",
                        "Penitentiary",
                        "LifeWithoutParole",
                        "BootCamp",
                        "Jail",
                        "Life",
                        "Death",
                        "ReverseSplit",
                        "ElectronicMonitoring",
                        "ConsecutiveSentence",
                        "CoterminousSentence",
                        "ChainGang",
                        "JailDiversion",
                        "InformalProbation",
                        "DuiSchool",
                        "DefensiveDrivingSchool",
                        "DocDrugProgram",
                        "BadCheckSchool",
                        "CourtReferralProgram",
                        "CommunityServiceHrs",
                        "DrugNearProject",
                        "SexOffenderCommunityNotification",
                        "DrugsNearSchool",
                        "HabitualOffender",
                        "HabitualOffenderNumber",
                        "VictimDOB",
                        "Drug",
                        "DrugCode",
                        "DrugVolume",
                        "DrugMeasureUnit",
                    )
            self._sentences = df
            return self._sentences

    def settings(self, debug=False):
        """
        Make settings table.
        """
        if debug:
            self._settings = None
        # if previously called with debug=True, reset
        if isinstance(self._settings, pl.DataFrame):
            if "Settings" in self._settings.columns:
                self._settings = None
        if isinstance(self._settings, pl.DataFrame):
            return self._settings
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing settings…"):
                df = self.archive.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"Description\:\s*\n\s*(?s)Settings(.+?)Court Action"
                        )
                        .str.split("\n")
                        .alias("Settings"),
                    ]
                )
                df = df.explode("Settings")
                df = df.with_columns(pl.col("Settings").str.strip())
                df = df.filter(pl.col("Settings").str.contains(r"^DOB|SSN").is_not())
                df = df.filter(pl.col("Settings").str.contains(r"00/00").is_not())
                df = df.filter(
                    pl.col("Settings").str.contains(r"^\d\d?/\d\d?/\d\d\d\d").is_not()
                )
                df = df.filter(pl.col("Settings").str.contains(r"[A-Z]"))
                df = df.filter(pl.col("Settings").str.contains("Date").is_not())
                df = df.filter(pl.col("Settings").is_null().is_not())
                df = df.filter(pl.col("Settings").str.contains(r"[a-z]").is_not())
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Settings")
                        .str.extract(r"^(\d) ")
                        .cast(pl.Int64, strict=False)
                        .alias("Number"),
                        pl.col("Settings")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Date"),
                        pl.col("Settings")
                        .str.extract(r"\d\d?/\d\d?/\d\d\d\d (\d\d\d)")
                        .alias("Que"),
                        pl.col("Settings")
                        .str.extract(
                            r"\d\d?/\d\d?/\d\d\d\d \d\d\d (\d\d?\:\d\d (AM|PM)?)",
                            group_index=1,
                        )
                        .alias("Time"),
                        pl.col("Settings")
                        .str.extract(
                            r"\d\d?/\d\d?/\d\d\d\d \d\d\d \d\d?\:\d\d (AM|PM)?(.+)",
                            group_index=2,
                        )
                        .str.strip()
                        .alias("Description"),
                    ]
                )
                if not debug:
                    df = df.select(
                        ["CaseNumber", "Number", "Date", "Que", "Time", "Description"]
                    )
            self._settings = df
            return self._settings

    def case_action_summary(self, debug=False):
        """
        Make case action summary table.
        """
        if debug:
            self._case_action_summary = None
        # if previously called with debug=True, reset
        if isinstance(self._case_action_summary, pl.DataFrame):
            if "Row" in self._case_action_summary.columns:
                self._case_action_summary = None
        if isinstance(self._case_action_summary, pl.DataFrame):
            return self._case_action_summary
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing case action summaries…"):
                df = self.archive.select("AllPagesText", "CaseNumber")
                df = df.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)Case Action Summary(.+) Date")
                    .str.replace(r"\s*\n\s*Operator\s*", "")
                    .alias("CAS"),
                )
                df = df.with_columns(
                    pl.col("CAS").apply(
                        lambda x: re.split(r"(\d\d?/\d\d?/\d\d\d\d)\s*\n", x)
                    )
                )
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("CAS").apply(lambda x: x[0::2][0:-1]).alias("Row"),
                        pl.col("CAS").apply(lambda x: x[1::2]).alias("Date"),
                    ]
                )
                df = df.explode("Row", "Date")
                df = df.with_columns(
                    pl.col("Row")
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.strip()
                )
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Date").str.to_date("%m/%d/%Y", strict=False),
                        pl.col("Row")
                        .str.extract(r"^(\w |\w\w\w |\w\w\w\d\d\d )")
                        .str.strip()
                        .alias("Operator"),
                        pl.col("Row")
                        .str.extract(
                            r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+) (\d\d?:\d\d [AP]M)",
                            group_index=2,
                        )
                        .str.replace("\n", "")
                        .str.strip()
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(
                            r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+) (\d\d?:\d\d [AP]M)",
                            group_index=3,
                        )
                        .alias("Code"),
                        pl.col("Row")
                        .str.extract(
                            r"(?s)^(\w |\w\w\w |\w\w\w\d\d\d )?(.+?) ([A-Z0-9-]+) (\d\d?:\d\d [AP]M)",
                            group_index=4,
                        )
                        .alias("Time"),
                    ]
                )
                if not debug:
                    df = df.select(
                        [
                            "CaseNumber",
                            "Date",
                            "Operator",
                            "Description",
                            "Code",
                            "Time",
                        ]
                    )
                df = df.filter(pl.col("Description").is_null().is_not())
            self._case_action_summary = df
            return self._case_action_summary

    def financial_history(self, debug=False):
        """
        Make financial history table.
        """
        if debug:
            self._financial_history = None
        # if previously called with debug=True, reset
        if isinstance(self._financial_history, pl.DataFrame):
            if "Row" in self._financial_history.columns:
                self._financial_history = None
        if isinstance(self._financial_history, pl.DataFrame):
            return self._financial_history
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing financial history…"):
                df = self.archive.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Financial History(.+?)Requesting Party")
                        .str.replace_all(
                            r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", ""
                        )
                        .str.replace(
                            r"(?s)\s*\n Description From Party To Party Admin Fee\s*\n\s*Money Type\s*\n\s*Reason Disbursement Accoun\s*\n\s*Transaction Batch\s*\n\s*Operator\s*\n\s*",
                            "",
                        )
                        .str.replace(
                            r"(?s)\s*Transaction Date\s*\n\s*Attorney Receipt Number Amount Description From Party To Party Admin Fee\s*\n\s*Money Type\s*\n\s*Reason Disbursement Accoun\s*\n\s*Transaction Batch\s*\n\s*Operator\s*\n\s*",
                            "",
                        )
                        .str.replace(r"(?s)\s*\n\s*SJIS Witness List\s*\n\s*", "")
                        .alias("FinancialHistory"),
                    ]
                )
                df = df.drop_nulls("FinancialHistory")
                df = df.with_columns(
                    [
                        pl.col("FinancialHistory").apply(
                            lambda x: re.split(r"(\d\d/\d\d/\d\d\d\d)", x)
                        )
                    ]
                )
                df = df.with_columns(
                    [
                        pl.col("FinancialHistory")
                        .apply(lambda x: x[0::2][1:])
                        .alias("Row"),
                        pl.col("FinancialHistory")
                        .apply(lambda x: x[1::2])
                        .alias("TransactionDate"),
                    ]
                )
                df = df.explode("Row", "TransactionDate")
                df = df.with_columns(
                    [
                        pl.col("Row")
                        .str.replace_all("\n", "")
                        .str.replace_all(" +", " ")
                        .str.replace_all(r"\. ", ".")
                        .str.strip()
                        .str.replace(r"CHANGED ?\w?$", "")
                        .str.replace(r"DELETED$", "")
                        .str.replace(r"CHECK ?\w?$", "")
                        .str.replace(r" \w$", "")
                        .str.strip(),
                        pl.col("TransactionDate").str.to_date("%m/%d/%Y", strict=False),
                    ]
                )
                df = df.with_columns(
                    [
                        pl.col("Row")
                        .str.extract(r"(.+?) \$")
                        .str.replace("REMITTANC E", "REMITTANCE")
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(r"\$([\d,]+\.\d+)")
                        .str.replace_all(r",", "")
                        .cast(pl.Float64, strict=False)
                        .alias("Amount"),
                        pl.col("Row")
                        .str.extract(r"\$([\d,]+\.\d+) ([^\s]{4})", group_index=2)
                        .alias("FromParty"),
                        pl.col("Row")
                        .str.extract(
                            r"\$([\d,]+\.\d+) ([^\s]{4}) ([^\s]{3,4})", group_index=3
                        )
                        .alias("ToParty"),
                        pl.col("Row")
                        .str.extract(r" (Y|N) ([^\s]{4}) (\d{8,})", group_index=1)
                        .alias("AdminFee"),
                        pl.col("Row")
                        .str.extract(r" ([^\s]{4}) (\d{8,})", group_index=1)
                        .alias("DisbursementAccount"),
                        pl.col("Row").str.extract(r"(\d{8,})").alias("ReceiptNumber"),
                        pl.col("Row")
                        .str.extract(r"(\d{8,}) (\d+)", group_index=2)
                        .alias("TransactionBatch"),
                        pl.col("Row")
                        .str.extract(r"(\w{3})( \w)?$", group_index=1)
                        .alias("Operator"),
                    ]
                )
                df = df.with_columns(
                    pl.col("Description").str.extract(r" (\w)$").alias("Reason")
                )
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "TransactionDate",
                        "Description",
                        "DisbursementAccount",
                        "TransactionBatch",
                        "ReceiptNumber",
                        "Amount",
                        "FromParty",
                        "ToParty",
                        "AdminFee",
                        "Reason",
                        "Operator",
                    )
            self._financial_history = df
            return self._financial_history

    def witnesses(self, debug=False):
        """
        Make witnesses table.
        """
        if debug:
            self._witnesses = None
        # if previously called with debug=True, reset
        if isinstance(self._witnesses, pl.DataFrame):
            if "Row" in self._witnesses.columns:
                self._witnesses = None
        if isinstance(self._witnesses, pl.DataFrame):
            return self._witnesses
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing witnesses tables…"):
                df = self.archive.select(
                    pl.col("CaseNumber"),
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?s)SJIS Witness List\s*\n\s*Date Issued\s*\n\s*Subpoena(.+?)Date"
                    )
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.replace(r"Requesting Party Witness # Name", "")
                    .alias("Witnesses"),
                )
                df = df.with_columns(
                    pl.col("Witnesses").apply(
                        lambda x: re.split(r"( [A-Z0-9]{4}\s*\n)", x)
                    )
                )
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Witnesses").apply(lambda x: x[0::2][0:-1]).alias("Row"),
                        pl.col("Witnesses").apply(lambda x: x[1::2]).alias("Witness#"),
                    ]
                )
                df = df.explode("Row", "Witness#")
                df = df.with_columns(
                    [
                        pl.col("Witness#").str.replace("\n", "").str.strip(),
                        pl.col("Row")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace_all("\n", "")
                        .str.replace_all(r"\s+", " ")
                        .str.strip(),
                    ]
                )
                df = df.filter(pl.col("Row").str.contains(r"[A-Za-z]"))
                df = df.with_columns(
                    [
                        pl.col("Row")
                        .str.extract(
                            r"(.+?)( [A-Z]?\d\d\d|$|\d\d/\d\d/\d\d\d\d)", group_index=1
                        )
                        .str.replace(
                            r"SERVED PERSONALLY |OTHER |CERTIFIED MAIL |PROCESS SERVER ",
                            "",
                        )
                        .str.strip()
                        .alias("Name"),
                        pl.col("Row")
                        .str.extract(
                            r"(SERVED PERSONALLY|OTHER|CERTIFIED MAIL|PROCESS SERVER)"
                        )
                        .alias("ServiceType"),
                        pl.col("Row")
                        .str.extract(r" ([A-Z]?\d\d\d)")
                        .alias("RequestingParty"),
                        pl.col("Row")
                        .str.extract(
                            r" [A-Z]?\d\d\d (SHERIFF|VIDEO|PROCESS SERVER|CERTIFIED|OTHER)"
                        )
                        .alias("IssuedType"),
                        pl.col("Row")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d) \d\d/\d\d/\d\d\d\d")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DateServed"),
                        pl.col("Row")
                        .str.extract(r"(\d\d/\d\d/\d\d\d\d)$")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("DateIssued"),
                    ]
                )
                df = df.filter(pl.col("Witness#").is_null().is_not())
                if not debug:
                    df = df.select(
                        "CaseNumber",
                        "Witness#",
                        "Name",
                        "RequestingParty",
                        "DateIssued",
                        "IssuedType",
                        "DateServed",
                        "ServiceType",
                    )
            self._witnesses = df
            return self._witnesses

    def attorneys(self, debug=False):
        """
        Make attorneys table.
        """
        if debug:
            self._attorneys = None
        # if previously called with debug=True, reset
        if isinstance(self._attorneys, pl.DataFrame):
            if "Attorneys" in self._attorneys.columns:
                self._attorneys = None
        if isinstance(self._attorneys, pl.DataFrame):
            return self._attorneys
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing attorneys tables…"):
                df = self.archive.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Attorney Code\s*\n\s*(.+?)Warrant")
                        .alias("Attorneys"),
                    ]
                )
                df = df.drop_nulls("Attorneys")
                df = df.with_columns(
                    pl.col("Attorneys").apply(
                        lambda x: re.split(r"(\s[A-Z0-9]{6}\s+\n)", x)
                    )
                )
                df = df.with_columns(
                    [
                        pl.col("Attorneys").apply(lambda x: x[0::2][0:-1]).alias("Row"),
                        pl.col("Attorneys")
                        .apply(lambda x: x[1::2])
                        .alias("AttorneyCode"),
                    ]
                )
                df = df.explode("Row", "AttorneyCode")
                df = df.with_columns(
                    pl.col("Row").str.replace_all("\n", "").str.strip()
                )
                df = df.filter(
                    pl.col("Row")
                    .str.replace(r"Attorney|Prosecutor", "")
                    .str.contains(r"[a-z]")
                    .is_not()
                )
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Row")
                        .str.extract(r"(Attorney \d+|Prosecutor \d+)$")
                        .alias("Number"),
                        pl.col("AttorneyCode").str.strip(),
                        pl.col("Row").str.extract(r"^(\w-\w+)").alias("TypeOfCounsel"),
                        pl.col("Row")
                        .str.extract(
                            r"^(\w-\w+)?(.+?) ([^\s]+\s*@|\(\d)", group_index=2
                        )
                        .str.strip()
                        .alias("Name"),
                        pl.col("Row")
                        .str.extract(
                            r"([^\s]+\s*@\s*[^\.]+\s*\.\s*[^\s]+)", group_index=1
                        )
                        .str.replace_all(r" ", "")
                        .alias("Email"),
                        pl.col("Row")
                        .str.extract(
                            r"(\(\d\d\d\) \d\d\d-\d\d\d\d) (Attorney \d+|Prosecutor \d+)",
                            group_index=1,
                        )
                        .alias("Phone"),
                    ]
                )
                # fix P-PUBLIC with DEFENDER in name
                df = df.with_columns(
                    pl.when(pl.col("TypeOfCounsel") == "P-PUBLIC")
                    .then(pl.col("Name").str.replace(r"^DEFENDER ", "").str.strip())
                    .otherwise(pl.col("Name"))
                    .alias("Name"),
                    pl.when(pl.col("TypeOfCounsel") == "P-PUBLIC")
                    .then(pl.lit("P-PUBLIC DEFENDER"))
                    .otherwise(pl.col("TypeOfCounsel"))
                    .alias("TypeOfCounsel"),
                )
                # fix S-PRO with SE in name
                df = df.with_columns(
                    pl.when(pl.col("TypeOfCounsel") == "S-PRO")
                    .then(pl.col("Name").str.replace(r"^SE ", "").str.strip())
                    .otherwise(pl.col("Name"))
                    .alias("Name"),
                    pl.when(pl.col("TypeOfCounsel") == "S-PRO")
                    .then(pl.lit("S-PRO SE"))
                    .otherwise(pl.col("TypeOfCounsel"))
                    .alias("TypeOfCounsel"),
                )
                # fix missing PRO SE names
                df = df.with_columns(
                    pl.when(
                        pl.col("Name").is_null() & pl.col("Row").str.contains("PRO SE")
                    )
                    .then(pl.lit("PRO SE"))
                    .otherwise(pl.col("Name"))
                    .alias("Name")
                )
                if not debug:
                    df = df.select(
                        [
                            "CaseNumber",
                            "Number",
                            "AttorneyCode",
                            "TypeOfCounsel",
                            "Name",
                            "Email",
                            "Phone",
                        ]
                    )
            self._attorneys = df
            return self._attorneys

    def images(self, debug=False):
        """
        Make images table.
        """
        if debug:
            self._images = None
        # if previously called with debug=True, reset
        if isinstance(self._images, pl.DataFrame):
            if "Row" in self._images.columns:
                self._images = None
        if isinstance(self._images, pl.DataFrame):
            return self._images
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing images tables…"):
                df = self.archive.with_columns(
                    [
                        pl.col("AllPagesText")
                        .str.extract(r"(?s)Images(.+)END OF THE REPORT")
                        .str.replace(r"\n Pages\s*", "")
                        .alias("Images")
                    ]
                )
                df = df.select(
                    pl.col("CaseNumber"),
                    pl.col("Images").apply(
                        lambda x: re.split(r"(\d\d?:\d\d:\d\d [AP]M)", x)
                    ),
                )
                df = df.select(
                    pl.col("CaseNumber"),
                    pl.col("Images").apply(lambda x: x[0::2][0:-1]).alias("Row"),
                    pl.col("Images").apply(lambda x: x[1::2]).alias("Time"),
                )
                df = df.explode("Row", "Time")
                df = df.with_columns(
                    [
                        pl.col("Row")
                        .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                        .str.replace(r"Date: Description Doc# Title  \n Images", "")
                        .str.replace_all(r"\n", " ")
                        .str.strip(),
                        pl.col("Time").str.strip(),
                    ]
                )
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Row")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Date"),
                        pl.col("Time"),
                        pl.col("Row")
                        .str.extract(r"\d+ [^0-9]+ (\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Doc#"),
                        pl.col("Row")
                        .str.extract(r"\d+ ([^0-9]+)")
                        .str.strip()
                        .alias("Title"),
                        pl.col("Row")
                        .str.extract(r"(?s)\d+ [^0-9]+ \d+ (.+) \d\d?/\d\d?/\d\d\d\d$")
                        .alias("Description"),
                        pl.col("Row")
                        .str.extract(r"^(\d+)")
                        .cast(pl.Int64, strict=False)
                        .alias("Pages"),
                    ]
                )
                if not debug:
                    df = df.select(
                        [
                            "CaseNumber",
                            "Date",
                            "Time",
                            "Doc#",
                            "Title",
                            "Description",
                            "Pages",
                        ]
                    )
                df = df.drop_nulls("Date")
            self._images = df
            return self._images

    def restitution(self, debug=False):
        """
        Make restitution table.
        """
        if debug:
            self._restitution = None
        # if previously called with debug=True, reset
        if isinstance(self._restitution, pl.DataFrame):
            if "RestitutionRaw" in self._restitution.columns:
                self._restitution = None
        if isinstance(self._restitution, pl.DataFrame):
            return self._restitution
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing restitution tables…"):
                df = self.archive.select("CaseNumber", "AllPagesText")
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract_all(r"(?s)Restitution (.+?) (Programs|Split)")
                        .alias("RestitutionRaw"),
                    ]
                )
                df = df.explode("RestitutionRaw")
                df = df.with_columns(
                    pl.col("RestitutionRaw")
                    .str.replace("Restitution", "")
                    .str.replace("Programs", "")
                    .str.replace("Split", "")
                    .str.replace(r"Recipient Description Amount\s*\n", "")
                    .str.replace(r"Restitution\s*\n", "")
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.replace(r"(?s)Linked Cases.+", "")
                    .str.replace(r"(?s)Enhanced.+", "")
                    .str.replace(r"(?s)Chain Gang.+", "")
                    .str.strip()
                    .str.split("\n")
                    .alias("Restitution")
                )
                df = df.explode("Restitution")
                df = df.filter(pl.col("Restitution") != "")
                df = df.with_columns(pl.col("Restitution").str.strip())
                df = df.filter(pl.col("Restitution").str.contains(r"^\w \d+ \d+\.\d\d"))
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Restitution")
                        .str.extract(r"^(\w) ")
                        .alias("Restitution"),
                        pl.col("Restitution")
                        .str.extract(r"^\w ([^\s]+) ")
                        .cast(pl.Int64, strict=False)
                        .alias("Description"),
                        pl.col("Restitution")
                        .str.extract(r"\w [^\s]+ (\d+\.\d\d)")
                        .cast(pl.Float64, strict=False)
                        .alias("Amount"),
                        pl.col("Restitution")
                        .str.extract(r"\w [^\s]+ \d+\.\d\d ([A-Z0-9]+)")
                        .alias("Recipient"),
                    ]
                )
                if not debug:
                    df = df.select(
                        [
                            "CaseNumber",
                            "Recipient",
                            "Restitution",
                            "Description",
                            "Amount",
                        ]
                    )
            self._restitution = df
            return self._restitution

    def linked_cases(self, debug=False):
        """
        Make linked cases table.
        """
        if debug:
            self._linked_cases = None
        if isinstance(self._linked_cases, pl.DataFrame):
            if "LinkedCases" in self._linked_cases.columns:
                self._linked_cases = None
        if isinstance(self._linked_cases, pl.DataFrame):
            return self._linked_cases
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing linked cases tables…"):
                df = self.archive.select("CaseNumber", "AllPagesText")
                df = df.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract_all(
                            r"(?s)Linked Cases\s*\n\s*Sentencing Number Case Type Case Type Description CaseNumber(.+?)Enforcement|Sentence"
                        )
                        .alias("LinkedCases"),
                    ]
                )
                df = df.explode("LinkedCases")
                df = df.with_columns(
                    pl.col("LinkedCases")
                    .str.replace("Sentence", "")
                    .str.replace(r"Sentencing.+", "")
                    .str.replace("Linked Cases", "")
                    .str.replace("Enforcement", "")
                    .str.replace(r"(?s)\d\s*\n\s*Last Update.+", "")
                    .str.replace(r"..Alacourt\.com \d\d?/\d\d?/\d\d\d\d \d+", "")
                    .str.strip()
                    .str.split("\n")
                )
                df = df.explode("LinkedCases")
                df = df.with_columns(
                    pl.when(pl.col("LinkedCases") == "")
                    .then(None)
                    .otherwise(pl.col("LinkedCases"))
                    .alias("LinkedCases")
                )
                df = df.with_columns(pl.col("LinkedCases").str.strip())
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("LinkedCases")
                        .str.extract(r"^(\d+) ")
                        .cast(pl.Int64, strict=False)
                        .alias("SentencingNumber"),
                        pl.col("LinkedCases")
                        .str.extract(r"^\d+ (\w) ")
                        .alias("CaseType"),
                        pl.col("LinkedCases")
                        .str.extract(r"\d+ \w ([A-Z]+)")
                        .alias("CaseTypeDescription"),
                        pl.col("LinkedCases")
                        .str.extract(
                            r"\d+ \w [A-Z]+ (\d\d-\w\w-\d\d\d\d-\d\d\d\d\d\d\.\d\d)"
                        )
                        .alias("LinkedCaseNumber"),
                    ]
                )
                df = df.drop_nulls("LinkedCaseNumber")
                if not debug:
                    df = df.select(
                        [
                            "CaseNumber",
                            "SentencingNumber",
                            "CaseType",
                            "CaseTypeDescription",
                            "LinkedCaseNumber",
                        ]
                    )
            self._linked_cases = df
            return self._linked_cases

    def continuances(self, debug=False):
        """
        Make continuances table.
        """
        if debug:
            self._continuances = None
        if isinstance(self._continuances, pl.DataFrame):
            if "Continuances" in self._continuances.columns:
                self._continuances = None
        if isinstance(self._continuances, pl.DataFrame):
            return self._continuances
        else:
            if not self.is_read:
                self.read()
            with console.status("Parsing continuances tables…"):
                df = self.archive.select(
                    [
                        pl.col("CaseNumber"),
                        pl.col("AllPagesText")
                        .str.extract(
                            r"(?s)Continuances.+?Comments\s*\n(.+?)\s*\n\s*Court Action"
                        )
                        .str.split("\n")
                        .alias("Continuances"),
                    ]
                )
                df = df.explode("Continuances")
                df = df.with_columns(
                    pl.col("Continuances").str.replace_all(r"\s+", " ").str.strip()
                )
                df = df.with_columns(
                    [
                        pl.col("CaseNumber"),
                        pl.col("Continuances")
                        .str.extract(r"(\d\d?/\d\d?/\d\d\d\d)")
                        .str.to_date("%m/%d/%Y", strict=False)
                        .alias("Date"),
                        pl.col("Continuances")
                        .str.extract(r"\d\d?/\d\d?/\d\d\d\d (\d\d:\d\d:\d\d [AP]M)")
                        .alias("Time"),
                        pl.col("Continuances")
                        .str.extract(
                            r"\d\d?/\d\d?/\d\d\d\d \d\d:\d\d:\d\d [AP]M ([A-Z0-9]{4})"
                        )
                        .alias("Code"),
                        pl.col("Continuances")
                        .str.extract(
                            r"\d\d?/\d\d?/\d\d\d\d \d\d:\d\d:\d\d [AP]M [A-Z0-9]{4} (.+?) [^\s]+$"
                        )
                        .alias("Comments"),
                        pl.col("Continuances")
                        .str.extract(r"([^\s]+)$")
                        .alias("Operator"),
                    ]
                )
                df = df.filter(pl.col("Code").is_null().is_not())
                if not debug:
                    df = df.select(
                        ["CaseNumber", "Date", "Time", "Code", "Comments", "Operator"]
                    )
            self._continuances = df
            return self._continuances

    def tables(self, debug=False):
        """
        Make all tables and return dict.
        """
        return {
            "cases": self.cases(debug=debug),
            "filing-charges": self.filing_charges(debug=debug),
            "disposition-charges": self.disposition_charges(debug=debug),
            "fees": self.fees(debug=debug),
            "sentences": self.sentences(debug=debug),
            "financial-history": self.financial_history(debug=debug),
            "witnesses": self.witnesses(debug=debug),
            "attorneys": self.attorneys(debug=debug),
            "settings": self.settings(debug=debug),
            "restitution": self.restitution(debug=debug),
            "linked-cases": self.linked_cases(debug=debug),
            "continuances": self.continuances(debug=debug),
            "case-action-summary": self.case_action_summary(debug=debug),
            "images": self.images(debug=debug),
        }

    def summary(self, pairs):
        """
        Summarize charges and fees by impact on voting rights using a filled pairs template.
        """
        if isinstance(pairs, str):
            self._pairs = read(pairs)
        if "Search" in self._pairs.columns:
            self._pairs = self._pairs.select(
                [pl.col("Name"), pl.col("Search").alias("AIS / Unique ID")]
            )
            self._pairs = self._pairs.unique()
        if not self.is_read:
            self.read()
        cases = self.cases()
        dch = self.disposition_charges()
        fch = self.filing_charges()
        with console.status("Creating summary…"):
            cases = cases.select("CaseNumber", "Name", "DOB", "Race", "Sex")
            cases = cases.with_columns(
                [
                    pl.col("Race").cast(pl.Utf8, strict=False),
                    pl.col("Sex").cast(pl.Utf8, strict=False),
                ]
            )
            fch = fch.join(self._pairs, on="Name", how="outer")
            fch = fch.groupby("AIS / Unique ID").all()
            fch = fch.select(
                [
                    pl.col("AIS / Unique ID"),
                    pl.col("CERVCharge")
                    .list.count_match(True)
                    .alias("CERVChargesCount"),
                    pl.col("PardonToVoteCharge")
                    .list.count_match(True)
                    .alias("PardonToVoteChargesCount"),
                    pl.col("PermanentCharge")
                    .list.count_match(True)
                    .alias("PermanentChargesCount"),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("FilingCharges"),
                ]
            )
            conv = dch.filter("Conviction")
            conv = conv.join(self._pairs, on="Name", how="outer")
            conv = conv.groupby("AIS / Unique ID").all()
            conv = conv.select(
                [
                    pl.col("AIS / Unique ID"),
                    pl.col("Conviction")
                    .list.count_match(True)
                    .alias("ConvictionCount"),
                    pl.col("CERVConviction")
                    .list.count_match(True)
                    .alias("CERVConvictionCount"),
                    pl.col("PardonToVoteConviction")
                    .list.count_match(True)
                    .alias("PardonToVoteConvictionCount"),
                    pl.col("PermanentConviction")
                    .list.count_match(True)
                    .alias("PermanentConvictionCount"),
                    pl.col("PaymentToRestore").list.mean(),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("Convictions"),
                ]
            )
            vrr = dch.filter(
                pl.col("CERVConviction")
                | pl.col("PardonToVoteConviction")
                | pl.col("PermanentConviction")
            )
            vrr = vrr.join(self._pairs, on="Name", how="outer")
            vrr = vrr.groupby("AIS / Unique ID").all()
            vrr = vrr.select(
                [
                    pl.col("AIS / Unique ID"),
                    pl.col("ChargesSummary")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("DisqualifyingConvictions"),
                ]
            )
            cases = cases.join(self._pairs, on="Name", how="outer")
            cases = cases.groupby("AIS / Unique ID").all()
            cases = cases.join(vrr, on="AIS / Unique ID", how="outer")
            cases = cases.join(conv, on="AIS / Unique ID", how="outer")
            cases = cases.join(fch, on="AIS / Unique ID", how="outer")
            cases = cases.with_columns(
                [
                    pl.col("CaseNumber")
                    .list.join(", ")
                    .str.replace_all(r"null,?", "")
                    .str.strip()
                    .str.replace(r",$", "")
                    .str.replace_all(r"\s+", " ")
                    .alias("Cases")
                ]
            )
            cases = cases.with_columns(
                [
                    pl.when(
                        pl.col("CERVConvictionCount").eq(0)
                        & pl.col("PardonToVoteConvictionCount").eq(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                        & pl.col("Cases").str.lengths().gt(0)
                    )
                    .then(True)
                    .otherwise(False)
                    .alias("EligibleToVote"),
                    pl.when(
                        pl.col("CERVConvictionCount").gt(0)
                        & pl.col("PardonToVoteConvictionCount").eq(0)
                        & pl.col("PermanentConvictionCount").eq(0)
                    )
                    .then(True)
                    .otherwise(False)
                    .alias("NeedsCERV"),
                    pl.when(
                        pl.col("PardonToVoteConvictionCount")
                        > 0 & pl.col("PermanentConvictionCount").eq(0)
                    )
                    .then(True)
                    .otherwise(False)
                    .alias("NeedsPardon"),
                    pl.when(pl.col("PermanentConvictionCount").gt(0))
                    .then(True)
                    .otherwise(False)
                    .alias("PermanentlyDisqualified"),
                ]
            )
            cases = cases.with_columns(
                [
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("EligibleToVote"))
                    .alias("EligibleToVote"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("NeedsCERV"))
                    .alias("NeedsCERV"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("NeedsPardon"))
                    .alias("NeedsPardon"),
                    pl.when(pl.col("Cases").str.lengths().eq(0))
                    .then(None)
                    .otherwise(pl.col("PermanentlyDisqualified"))
                    .alias("PermanentlyDisqualified"),
                ]
            )
            cases = cases.select(
                [
                    pl.col("AIS / Unique ID"),
                    pl.col("Name").list.first(),
                    pl.col("DOB").list.first(),
                    pl.col("Race").list.first(),
                    pl.col("Sex").list.first(),
                    pl.col("PaymentToRestore"),
                    pl.col("EligibleToVote"),
                    pl.col("NeedsCERV"),
                    pl.col("NeedsPardon"),
                    pl.col("PermanentlyDisqualified"),
                    pl.col("ConvictionCount"),
                    pl.col("CERVChargesCount"),
                    pl.col("CERVConvictionCount"),
                    pl.col("PardonToVoteChargesCount"),
                    pl.col("PardonToVoteConvictionCount"),
                    pl.col("PermanentChargesCount"),
                    pl.col("PermanentConvictionCount"),
                    pl.col("DisqualifyingConvictions"),
                    pl.col("Convictions"),
                    pl.col("FilingCharges"),
                    pl.col("Cases"),
                ]
            )
            cases = cases.sort("Name")
        self._summary = cases
        return self._summary

    def pairs_template(self):
        """
        Create empty pairs template for summary() pairs parameter.
        """
        if not self.is_read:
            self.read()
        with console.status("Creating template…"):
            names = self.archive.with_columns(
                [
                    pl.col("AllPagesText")
                    .str.extract(
                        r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})([A-Z\s]{10,100})(Case Number)*",
                        group_index=1,
                    )
                    .str.replace_all("Case Number:", "", literal=True)
                    .str.replace(r"C$", "")
                    .str.strip()
                    .alias("Name"),
                    pl.col("AllPagesText")
                    .str.extract(r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", group_index=1)
                    .str.replace_all(r"[^\d/]", "")
                    .str.strip()
                    .str.to_date("%m/%d/%Y", strict=False)
                    .alias("DOB"),
                    pl.col("AllPagesText")
                    .str.extract(r"(?s)(SSN:)(.{0,100})(Alias 1)", group_index=2)
                    .str.strip()
                    .alias("Alias"),
                ]
            )
            names = (
                names.groupby("Name")
                .agg("CaseNumber", "Alias", "DOB")
                .select(
                    [
                        pl.lit("").alias("AIS / Unique ID"),
                        pl.col("Name"),
                        pl.col("Alias").list.get(0),
                        pl.col("DOB").list.get(0),
                        pl.col("CaseNumber").list.lengths().alias("CaseCount"),
                        pl.col("CaseNumber").list.join(", ").alias("Cases"),
                    ]
                )
            )
            names = names.sort("Name")
            names = names.filter(pl.col("Name") != "")
        self._pairs_template = names
        return self._pairs_template

    def write_tables(self, path):
        """
        Write all made tables to output path. If multiple tables, file extension must be .xlsx or .xls. Otherwise, .csv, .parquet, and .json are also supported.
        """
        all_tables = {
            "cases": self._cases,
            "filing-charges": self._filing_charges,
            "disposition-charges": self._disposition_charges,
            "fees": self._fees,
            "sentences": self._sentences,
            "financial-history": self._financial_history,
            "witnesses": self._witnesses,
            "attorneys": self._attorneys,
            "settings": self._settings,
            "restitution": self._restitution,
            "linked-cases": self._linked_cases,
            "continuances": self._continuances,
            "case-action-summary": self._case_action_summary,
            "images": self._images,
        }
        only_df_vars = {}
        for x in all_tables:
            if isinstance(all_tables[x], pl.DataFrame):
                only_df_vars.update({x: all_tables[x]})
        write(only_df_vars, path, log=True)
        return only_df_vars

    def write_archive(self, path):
        """
        Write case archive to output path. Supports .xls, .xlsx, .parquet, and .csv. Parquet export recommended.
        """
        if not self.is_read:
            self.read()
        cols = [
            col
            for col in ["CaseNumber", "Path", "Timestamp", "AllPagesText"]
            if col in self.archive.columns
        ]
        out = self.archive.select(cols)
        write({"archive": out}, path, log=True)
        return out


## COMMAND LINE INTERFACE


@app.command(no_args_is_help=True)
def party_search(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help="Path to queue table with one or more columns: 'Name', 'Party Type', 'SSN', 'DOB', 'County', 'Division', 'Case Year', 'Filed Before', 'Filed After', 'No Records'.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output results table. Will attempt to append to existing table at output path.",
            show_default=False,
        ),
    ],
    customer_ID: Annotated[
        str,
        typer.Option(
            "--customer-id",
            "-c",
            help="Customer ID for Alacourt login.",
            prompt="Customer ID",
            show_default=False,
        ),
    ],
    user_ID: Annotated[
        str,
        typer.Option(
            "--user-id",
            "-u",
            help="User ID for Alacourt login.",
            prompt="User ID",
            show_default=False,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="Password for Alacourt login.",
            prompt="Password",
            hide_input=True,
            show_default=False,
        ),
    ],
    criminal_only: Annotated[
        bool,
        typer.Option(
            "--criminal-only", help="Only search criminal cases.", show_default=False
        ),
    ] = False,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", help="Print detailed logs while working.", show_default=False
        ),
    ] = False,
):
    """
    Collect results from Alacourt Party Search into a table at `output_path`. Input `queue_path` table from .xls(x), .csv, .json, or .parquet with columns corresponding to Alacourt Party Search fields: 'Name', 'Party Type', 'SSN', 'DOB', 'County', 'Division', 'Case Year', 'Filed Before', 'Filed After', 'No Records'.
    """
    queue_path = os.path.abspath(queue_path)
    output_path = os.path.abspath(output_path)
    headless = not show_browser

    if os.path.splitext(queue_path)[1] not in (
        ".xls",
        ".xlsx",
        ".csv",
        ".json",
        ".parquet",
    ):
        raise Exception(
            "Queue path file extension not supported. Retry with .xls, .xlsx, .csv, .json, or .parquet."
        )
    if os.path.splitext(output_path)[1] not in (
        ".xls",
        ".xlsx",
        ".csv",
        ".json",
        ".parquet",
    ):
        raise Exception(
            "Output path file extension not supported. Retry with .xls, .xlsx, .csv, .json, or .parquet."
        )

    driver = AlacourtDriver(headless=headless)
    driver.login(customer_ID, user_ID, password)
    driver.start_party_search_queue(queue_path, output_path, criminal_only)


@app.command(no_args_is_help=True)
def fetch_cases(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help="Path to queue table with 'Case Number' column.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output directory. PDFs will populate directory as they download.",
            show_default=False,
        ),
    ],
    customer_ID: Annotated[
        str,
        typer.Option(
            "--customer-id",
            "-c",
            help="Customer ID for Alacourt login.",
            prompt="Customer ID",
            show_default=False,
        ),
    ],
    user_ID: Annotated[
        str,
        typer.Option(
            "--user-id",
            "-u",
            help="User ID for Alacourt login.",
            prompt="User ID",
            show_default=False,
        ),
    ],
    password: Annotated[
        str,
        typer.Option(
            "--password",
            "-p",
            help="Password for Alacourt login.",
            prompt="Password",
            hide_input=True,
            show_default=False,
        ),
    ],
    verify: Annotated[
        bool,
        typer.Option(
            help="Verify successful case downloads and reattempt failed downloads."
        ),
    ] = True,
    pre_verify: Annotated[
        bool,
        typer.Option(
            help="Check output directory for already downloaded cases before starting."
        ),
    ] = False,
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", help="Print detailed logs while working.", show_default=False
        ),
    ] = False,
):
    """
    From a queue table with 'Case Number' or 'CaseNumber' column, download case detail PDFs to directory at `output_path`.
    """
    queue_path = os.path.abspath(queue_path)
    output_path = os.path.abspath(output_path)
    headless = not show_browser

    if os.path.splitext(queue_path)[1] not in (
        ".xls",
        ".xlsx",
        ".csv",
        ".json",
        ".parquet",
    ):
        raise Exception(
            "Queue path file extension not supported. Retry with .xls, .xlsx, .csv, .json, or .parquet."
        )
    if not os.path.isdir(output_path):
        raise Exception("Output path must be valid directory.")

    driver = AlacourtDriver(output_path, headless=headless)
    driver.login(customer_ID, user_ID, password)
    driver.start_case_number_queue(
        queue_path, verbose=verbose, verify=verify, pre_verify=pre_verify
    )


@app.command(no_args_is_help=True)
def crawl_adoc(
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xls, .xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
):
    """
    Collect full inmates list from ADOC Inmate Search and write to table at `output_path` (.xls, .xlsx, .csv, .json, .parquet).
    """
    output_path = os.path.abspath(output_path)
    headless = not show_browser

    driver = ADOCDriver(output_path, headless)
    driver.crawl(output_path)


@app.command(no_args_is_help=True)
def search_adoc(
    queue_path: Annotated[
        Path,
        typer.Argument(
            help="Path to queue table with 'First Name', 'Last Name', and 'AIS' columns.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xls, .xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
    show_browser: Annotated[
        bool,
        typer.Option(
            "--show-browser",
            help="Show browser window while working.",
            show_default=False,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose", help="Print detailed logs while working.", show_default=False
        ),
    ] = False,
):
    """
    Search ADOC using queue with 'First Name', 'Last Name', and 'AIS' columns to retrieve sentencing information from ADOC. Record table to `output_path`.
    """
    queue_path = os.path.abspath(queue_path)
    output_path = os.path.abspath(output_path)
    headless = not show_browser

    driver = ADOCDriver(output_path, headless)
    driver.start_queue(queue_path, output_path, verbose=verbose)


@app.command(no_args_is_help=True)
def make_archive(
    directory_path: Annotated[
        Path, typer.Argument(help="Path to PDF case directory.", show_default=False)
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output archive (recommend .parquet).", show_default=False
        ),
    ],
):
    """
    Create case text archive from directory of case detail PDFs.
    """
    directory_path = os.path.abspath(directory_path)
    output_path = os.path.abspath(output_path)

    cases = Cases(str(directory_path))
    cases.write_archive(str(output_path))


@app.command(no_args_is_help=True)
def make_table(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xls, .xlsx, .csv, .json, .parquet). `All` table export must output to .xls or .xlsx.",
            show_default=False,
        ),
    ],
    table: Annotated[
        str,
        typer.Option(
            "--table",
            "-t",
            help="Output table selection: all, cases, filing-charges, disposition-charges, fees, attorneys, case-action-summary, financial-history, images, sentences, settings, witnesses, restitution, linked-cases, continuances.",
            show_default=True,
        ),
    ] = "all",
):
    """
    Create table at `output_path` from archive or directory at `input_path`.
    """
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    if table == "all" and os.path.splitext(output_path)[1] not in (".xls", ".xlsx"):
        raise Exception(
            "Must select a table to export using --table flag. Options: cases, filing-charges, disposition-charges, fees, attorneys, case-action-summary, financial-history, images, sentences, settings, witnesses, restitution, linked-cases, continuances."
        )

    cases = Cases(str(input_path))
    cases.read()

    if table == "all":
        output = cases.tables()
    elif table == "cases":
        output = cases.cases()
    elif table == "fees":
        output = cases.fees()
    elif table == "filing-charges":
        output = cases.filing_charges()
    elif table == "disposition-charges":
        output = cases.disposition_charges()
    elif table == "attorneys":
        output = cases.attorneys()
    elif table == "case-action-summary":
        output = cases.case_action_summary()
    elif table == "financial-history":
        output = cases.financial_history()
    elif table == "images":
        output = cases.images()
    elif table == "sentences":
        output = cases.sentences()
    elif table == "settings":
        output = cases.settings()
    elif table == "witnesses":
        output = cases.witnesses()
    elif table == "restitution":
        output = cases.restitution()
    elif table == "linked-cases":
        output = cases.linked_cases()
    elif table == "continuances":
        output = cases.continuances()
    else:
        raise Exception(
            "Invalid table selection. Options: all, cases, filing-charges, disposition-charges, fees, attorneys, case-action-summary, financial-history, images, sentences, settings, witnesses, restitution, linked-cases, continuances."
        )

    write(output, output_path, log=True)


@app.command(no_args_is_help=True)
def make_summary(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    pairs_path: Annotated[
        Path,
        typer.Argument(
            help="Path to filled pairs template or party search results table.",
            show_default=False,
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xls, .xlsx, .csv, .json, .parquet).",
            show_default=False,
        ),
    ],
):
    """
    Create voting rights summary grouped by person using a completed name/AIS pairing template (use make-template to create empty template).
    """
    input_path = os.path.abspath(input_path)
    pairs_path = os.path.abspath(pairs_path)
    output_path = os.path.abspath(output_path)

    cases = Cases(input_path)
    output = cases.summary(pairs_path)
    write({"summary": output}, output_path)


@app.command(no_args_is_help=True)
def make_template(
    input_path: Annotated[
        Path,
        typer.Argument(
            help="Path to input case directory or archive.", show_default=False
        ),
    ],
    output_path: Annotated[
        Path,
        typer.Argument(
            help="Path to output table (.xls, .xlsx, .csv, .json, .parquet). `All` table export must output to .xls or .xlsx.",
            show_default=False,
        ),
    ],
):
    """
    Create empty pairing template to be used as input for make-summary to create a voting rights summary grouped by person instead of by case.
    """
    input_path = os.path.abspath(input_path)
    output_path = os.path.abspath(output_path)

    cases = Cases(input_path)
    output = cases.pairs_template()
    write({"pairs-template": output}, output_path)


@app.command(no_args_is_help=True)
def rename_cases(
    input_directory: Annotated[
        Path, typer.Argument(help="Directory to rename cases within.")
    ]
):
    """
    Rename all cases in a directory to full case number. Duplicates will be removed.
    """
    input_directory = os.path.abspath(input_directory)
    pdfs = glob.glob(input_directory + "**/*.pdf", recursive=True)
    progress_bar = Progress(*Progress.get_default_columns(), MofNCompleteColumn())
    with progress_bar as p:
        for pdf in p.track(pdfs, description="Renaming PDFs…"):
            doc = fitz.open(pdf)
            text = " \n ".join(
                x[4].replace("\n", " ") for x in doc[0].get_text(option="blocks")
            )
            cnum = (
                re.search(r"County: (\d\d)", str(text)).group(1)
                + "-"
                + re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text)).group()
            )
            newpath = f"{os.path.split(pdf)[0]}/{cnum}.pdf"
            os.rename(pdf, newpath)


def version_callback(value: bool):
    if value:
        print(f"Alacorder {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", callback=version_callback, help="Show the version and exit."
    )
):
    pass


if __name__ == "__main__":
    app()


## GETTERS


def getName(text):
    try:
        return (
            re.sub(
                r"Case Number:",
                "",
                re.search(
                    r"(?:VS\.|V\.| VS | V | VS: |-VS-{1})(.{0,100})(Case Number)*",
                    str(text),
                ).group(1),
            )
            .rstrip("C")
            .strip()
        )
    except:
        return ""


def getAlias(text):
    try:
        return re.sub(
            r":", "", re.search(r"(?:SSN)(.{5,75})(?:Alias)", str(text)).group(1)
        ).strip()
    except:
        return ""


def getDOB(text):
    try:
        return datetime.strptime(
            re.sub(
                r"[^\d/]",
                "",
                re.search(r"(\d{2}/\d{2}/\d{4})(?:.{0,5}DOB:)", str(text)).group(1),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getPhone(text):
    try:
        text = str(text)
        text = re.sub(r"[^0-9]", "", re.search(r"(Phone: )(.+)", text).group(2)).strip()
        if len(text) < 7 or text[0:10] == "2050000000":
            return ""
        elif len(text) > 10:
            return text[0:10]
        else:
            return text
    except:
        return ""


def getRace(text):
    try:
        return re.search(r"(B|W|H|A)/(F|M)", str(text)).group(1)
    except:
        return ""


def getSex(text):
    try:
        return re.search(r"(B|W|H|A)/(F|M)", str(text)).group(2)
    except:
        return ""


def getAddress1(text):
    try:
        return re.sub(
            r"Phone.+",
            "",
            re.search(r"(?:Address 1:)(.+)(?:Phone)*?", str(text)).group(1),
        ).strip()
    except:
        return ""


def getAddress2(text):
    try:
        return re.sub(
            r"Defendant Information|JID:.+",
            "",
            re.search(r"(?:Address 2:)(.+)", str(text)).group(1).strip(),
        )
    except:
        return ""


def getCity(text):
    try:
        return re.search(r"(?:City: )(.*)(?:State: )(.*)", str(text)).group(1)
    except:
        return ""


def getState(text):
    try:
        return re.search(r"(?:City: )(.*)(?:State: )(.*)", str(text)).group(2)
    except:
        return ""


def getCountry(text):
    try:
        return re.sub(
            r"Country:",
            "",
            re.sub(
                r"(Enforcement|Party|Country)",
                "",
                re.search(r"Country: (\w*+)", str(text)).group(),
            ).strip(),
        )
    except:
        return ""


def getZipCode(text):
    try:
        return re.sub(
            r"-0000$|[A-Z].+", "", re.search(r"(Zip: )(.+)", str(text)).group(2)
        ).strip()
    except:
        return ""


def getAddress(text):
    try:
        street1 = re.sub(
            r"Phone.+",
            "",
            re.search(r"(?:Address 1:)(.+)(?:Phone)*?", str(text)).group(1),
        ).strip()
    except:
        street1 = ""
    try:
        street2 = getAddress2(text).strip()
    except:
        street2 = ""
    try:
        zipcode = re.sub(
            r"[A-Z].+", "", re.search(r"(Zip: )(.+)", str(text)).group(2)
        ).strip()
    except:
        zipcode = ""
    try:
        city = re.search(r"(?:City: )(.*)(?:State: )(.*)", str(text)).group(1).strip()
    except:
        city = ""
    try:
        state = re.search(r"(?:City: )(.*)(?:State: )(.*)", str(text)).group(2).strip()
    except:
        state = ""
    if len(city) > 3:
        return f"{street1} {street2} {city}, {state} {zipcode}".strip()
    else:
        return f"{street1} {street2} {city} {state} {zipcode}".strip()


def getTotalRow(text):
    try:
        mmm = re.search(r"(Total:.+\$[^\n]*)", str(text)).group()
        mm = re.sub(r"[^0-9|\.|\s|\$]", "", str(mmm))
        m = re.findall(r"\d+\.\d{2}", str(mm))
        return m
    except:
        return ["0.00", "0.00", "0.00", "0.00"]


def getTotalAmtDue(text):
    try:
        return float(re.sub(r"[\$\s]", "", getTotalRow(text)[0]))
    except:
        return 0.00


def getTotalAmtPaid(text):
    try:
        return float(re.sub(r"[\$\s]", "", getTotalRow(text)[1]))
    except:
        return 0.00


def getTotalBalance(text):
    try:
        return float(re.sub(r"[\$\s]", "", getTotalRow(text)[2]))
    except:
        return 0.00


def getTotalAmtHold(text):
    try:
        return float(re.sub(r"[\$\s]", "", getTotalRow(text)[3]))
    except:
        return 0.00


def getPaymentToRestore(text):
    try:
        tbal = getTotalBalance(text)
    except:
        return 0.0
    try:
        d999mm = re.search(r"(ACTIVE[^\n]+D999[^\n]+)", str(text)).group()
        d999m = re.findall(r"\$\d+\.\d{2}", str(d999mm))
        d999 = float(re.sub(r"[\$\s]", "", d999m[-1]))
    except:
        d999 = 0.0
    return float(tbal - d999)


def getShortCaseNumber(text):
    try:
        return re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text)).group()
    except:
        return ""


def getCounty(text):
    try:
        return re.search(r"County: (\d\d)", str(text)).group(1)
    except:
        return ""


def getCaseNumber(text):
    try:
        return (
            re.search(r"County: (\d{2})", str(text)).group(1)
            + "-"
            + re.search(r"(\w{2}\-\d{4}-\d{6}\.\d{2})", str(text)).group()
        )
    except:
        return ""


def getCaseYear(text):
    try:
        return int(re.search(r"\w{2}\-(\d{4})-\d{6}\.\d{2}", str(text)).group(1))
    except:
        return None


def getLastName(text):
    try:
        return getName(text).split(" ")[0].strip()
    except:
        return ""


def getFirstName(text):
    try:
        return getName(text).split(" ")[-1].strip()
    except:
        return ""


def getMiddleName(text):
    try:
        if len(getName(text).split(" ")) > 2:
            return " ".join(getName(text).split(" ")[1:-2]).strip()
        else:
            return ""
    except:
        return ""


def getRelatedCases(text):
    try:
        return re.search(r"Related Cases: (.+)", str(text)).group(1).strip()
    except:
        return ""


def getFilingDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"Filing Date: ",
                "",
                re.search(r"Filing Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getCaseInitiationDate(text):
    try:
        return datetime.strptime(
            re.search(r"Case Initiation Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(
                1
            ),
            "%m/%d/%Y",
        )
    except:
        return None


def getArrestDate(text):
    try:
        return datetime.strptime(
            re.search(r"Arrest Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getOffenseDate(text):
    try:
        return datetime.strptime(
            re.search(r"Offense Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getIndictmentDate(text):
    try:
        return datetime.strptime(
            re.search(r"Indictment Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getYouthfulDate(text):
    try:
        return datetime.strptime(
            re.search(r"Youthful Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getRetrieved(text):
    try:
        return datetime.strptime(
            re.search(r"Alacourt\.com (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getCourtAction(text):
    try:
        return re.sub(
            "DOCKETED",
            "DOCKETED BY MISTAKE",
            re.search(
                r"Court Action: (WAIVED TO GJ \d\d/\d\d/\d\d\d\d|WAIVED TO GJ|GUILTY PLEA|NOT GUILTY/INSAN E|GJ|DISMISSED W/CONDITION S|DISMISSED/N OL PROS W/CONDITION S|TIME LAPSED PRELIM\. FORWARDED TO GJ|TIME LAPSED|NOL PROSS|CONVICTED|INDICTED PRIOR TO ADJUDICATIO N|TRANSFERED ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? ?\(MUST MAKE OCS ENTRY TO EXPLAIN \)|OTHER \(MUST ?\d?\d?/?\d?\d?/?\d?\d?\d?\d? MAKE OCS ENTRY\)|FINAL BOND FORF\.|FORFEITURE SET ASIDE \(\.50 CASE\)|FINAL FORFEITURE \(\.50 CASE\)|DISMISSED|FORFEITURE|TRANSFER|REMANDED|WAIVED|ACQUITTED|WITHDRAWN|PETITION DENIED|COND\. FORF\. SET ASIDE|COND\. FORF\.|OTHER|PROBATION NT REVOKE|PROBATION/S|ANCTION|NO PROBABLE CAUSE|PETITION GRANTED|PROBATION TERMINATED|FINAL FORF\. SET ASIDE|DOCKETED|PROBATION NOT REVOKED \(\.70 CASE\)|PROBATION REVOKED \(\.70 CASE\)|PROBATION REVOKED|PRETRIAL DIVERSION|YOUTHFUL OFFENDER)",
                str(text),
            ).group(1),
        )
    except:
        return ""


def getCourtActionDate(text):
    try:
        return datetime.strptime(
            re.search(r"Court Action Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getDescription(text):
    try:
        return (
            re.search(r"Charge: ([A-Z\.0-9\-\s]+)", str(text))
            .group(1)
            .rstrip("C")
            .strip()
        )
    except:
        return ""


def getJuryDemand(text):
    try:
        return re.search(r"Jury Demand: ([A-Za-z]+)", str(text)).group(1).strip()
    except:
        return ""


def getALInstitutionalServiceNum(text):
    try:
        return re.search(r"(\d+)\s*\n\s*Youthful Date:", str(text)).group(1).strip()
    except:
        return ""


def getInpatientTreatmentOrdered(text):
    try:
        return (
            re.search(r"Inpatient Treatment Ordered: (YES|NO)", str(text))
            .group(1)
            .strip()
        )
    except:
        return ""


def getTrialType(text):
    try:
        return re.sub(
            r"\n?\s*P$", "", re.search(r"Trial Type: ([A-Z\s]+)", str(text)).group(1)
        ).strip()
    except:
        return ""


def getJudge(text):
    try:
        return re.search(r"Judge: (.+)", str(text)).group(1).strip()
    except:
        return ""


def getProbationOfficeNumber(text):
    try:
        return re.search(r"Probation Office \#: ([0-9\-]+)", str(text)).group(1).strip()
    except:
        return ""


def getDefendantStatus(text):
    try:
        return (
            re.search(r"Defendant Status: ([A-Z\s]+)", str(text))
            .group(1)
            .rstrip("J")
            .strip()
        )
    except:
        return ""


def getArrestingOfficer(text):
    try:
        return (
            re.search(r"Arresting Officer: (.+)", str(text))
            .group(1)
            .rstrip("S")
            .rstrip("P")
            .strip()
        )
    except:
        return ""


def getArrestingAgencyType(text):
    try:
        out = re.search(r"([^0-9]+) Arresting Agency Type:", str(text)).group(1)
    except:
        return ""
    out = re.sub(r"^\-.+", "", out)
    out = re.sub(r"County\:", "", out)
    out = re.sub(r"Defendant Status\:", "", out)
    out = re.sub(r"Judge\:", "", out)
    out = re.sub(r"Trial Type\:", "", out)
    out = re.sub(r"Probation Office \#\:", "", out)
    return out.strip()


def getProbationOfficeName(text):
    try:
        return (
            re.search(r"Probation Office Name: ([A-Z0-9]+)", str(text)).group(1).strip()
        )
    except:
        return ""


def getTrafficCitationNumber(text):
    try:
        return (
            re.search(r"Traffic Citation \#: ([A-Z0-9]+)", str(text)).group(1).strip()
        )
    except:
        return ""


def getPreviousDUIConvictions(text):
    try:
        return int(
            re.search(r"Previous DUI Convictions: (\d{3})", str(text)).group(1).strip()
        )
    except:
        return ""


def getCaseInitiationType(text):
    try:
        return (
            re.search(r"Case Initiation Type: ([A-Z\s]+)", str(text))
            .group(1)
            .rstrip("J")
            .strip()
        )
    except:
        return ""


def getDomesticViolence(text):
    try:
        return re.search(r"Domestic Violence: (YES|NO)", str(text)).group(1).strip()
    except:
        return ""


def getAgencyORI(text):
    try:
        return re.sub(
            r"\s+",
            " ",
            re.search(r"Agency ORI: ([A-Z\s-]+)", str(text)).group(1).rstrip("C"),
        ).strip()
    except:
        return ""


def getDriverLicenseNo(text):
    try:
        m = re.search(r"Driver License N°: (.+)", str(text)).group(1).strip()
        if m == "AL":
            return ""
        else:
            return m
    except:
        return ""


def getSSN(text):
    try:
        return re.search(r"([X\d]{3}\-[X\d]{2}-[X\d]{4})", str(text)).group(1).strip()
    except:
        return ""


def getStateID(text):
    try:
        return re.search(r"([A-Z0-9]{11}?) State ID:", str(text)).group(1).strip()
    except:
        return ""


def getWeight(text):
    try:
        return int(re.search(r"Weight: (\d+)", str(text)).group(1).strip())
    except:
        return ""


def getHeight(text):
    try:
        return re.search(r"Height : (\d'\d{2})", str(text)).group(1).strip() + '"'
    except:
        return ""


def getEyes(text):
    try:
        return re.search(r"Eyes/Hair: (\w{3})/(\w{3})", str(text)).group(1).strip()
    except:
        return ""


def getHair(text):
    try:
        return re.search(r"Eyes/Hair: (\w{3})/(\w{3})", str(text)).group(2).strip()
    except:
        return ""


def getWarrantIssuanceDate(text):
    try:
        return datetime.strptime(
            re.search(r"(\d\d?/\d\d?/\d\d\d\d) Warrant Issuance Date:", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getWarrantActionDate(text):
    try:
        return datetime.strptime(
            re.search(r"Warrant Action Date: (\d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getWarrantIssuanceStatus(text):
    try:
        return re.search(r"Warrant Issuance Status: (\w)", str(text)).group(1).strip()
    except:
        return ""


def getWarrantActionStatus(text):
    try:
        return re.search(r"Warrant Action Status: (\w)", str(text)).group(1).strip()
    except:
        return ""


def getWarrantLocationStatus(text):
    try:
        return re.search(r"Warrant Location Status: (\w)", str(text)).group(1).strip()
    except:
        return ""


def getWarrantIssuanceDescription(text):
    try:
        descs = re.search(
            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", str(text)
        ).group(1)
        return re.search(
            r"(ALIAS WARRANT|BENCH WARRANT|FAILURE TO PAY WARRANT|PROBATION WARRANT)",
            descs,
        ).group(1)
    except:
        return ""


def getWarrantActionDescription(text):
    try:
        descs = re.search(
            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", str(text)
        ).group(1)
        return re.search(
            r"(WARRANT RECALLED|WARRANT DELAYED|WARRANT RETURNED|WARRANT SERVED)", descs
        ).group(1)
    except:
        return ""


def getWarrantLocationDescription(text):
    try:
        descs = re.search(
            r"(?s)Bondsman Process Return: (.+?)(Number|Orgin)", str(text)
        ).group(1)
        return re.search(r"(CLERK'S OFFICE|LAW ENFORCEMENT)", descs).group(1)
    except:
        return ""


def getNumberOfWarrants(text):
    try:
        return (
            re.search(r"Number Of Warrants: (\d{3}\s\d{3})", str(text)).group(1).strip()
        )
    except:
        return ""


def getBondType(text):
    try:
        return re.search(r"Bond Type: (\w)", str(text)).group(1).strip()
    except:
        return ""


def getBondTypeDesc(text):
    try:
        return re.search(r"Bond Type Desc: ([A-Z\s]+)", str(text)).group(1).strip()
    except:
        return ""


def getBondAmount(text):
    try:
        return float(
            re.sub(
                r"[^0-9\.\s]",
                "",
                re.search(r"([\d\.]+) Bond Amount:", str(text)).group(1).strip(),
            )
        )
    except:
        return ""


def getSuretyCode(text):
    try:
        return re.sub(
            r"Release.+", "", re.search(r"Surety Code: (.+", str(text)).group(1).strip()
        ).strip()
    except:
        return ""


def getBondReleaseDate(text):
    try:
        return datetime.strptime(
            re.search(r"Release Date: (\d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getFailedToAppearDate(text):
    try:
        return datetime.strptime(
            re.search(r"Failed to Appear Date: (\d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getBondsmanProcessIssuance(text):
    try:
        return (
            re.search(
                r"Bondsman Process Issuance: ([^\n]*?) Bondsman Process Return:",
                str(text),
            )
            .group(1)
            .strip()
        )
    except:
        return ""


def getBondsmanProcessReturn(text):
    try:
        return datetime.strptime(
            re.sub(
                r"Number.+",
                "",
                re.search(r"Bondsman Process Return: (.+)", str(text)).group(1).strip(),
            ),
            "%m/%d/%Y",
        )
    except:
        return ""


def getAppealDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"[\n\s]",
                "",
                re.search(r"([\n\s/\d]*?) Appeal Court:", str(text)).group(1).strip(),
            ),
            "%m/%d/%Y",
        )
    except:
        return None


def getAppealCourt(text):
    try:
        return re.search(r"([A-Z\-\s]+) Appeal Case Number", str(text)).group(1).strip()
    except:
        return ""


def getOriginOfAppeal(text):
    try:
        return (
            re.search(r"Orgin Of Appeal: ([A-Z\-\s]+)", str(text))
            .group(1)
            .rstrip("L")
            .strip()
        )
    except:
        return ""


def getAppealToDesc(text):
    try:
        return (
            re.search(r"Appeal To Desc: ([A-Z\-\s]+)", str(text))
            .group(1)
            .rstrip("D")
            .rstrip("T")
            .strip()
        )
    except:
        return ""


def getAppealStatus(text):
    try:
        return (
            re.search(r"Appeal Status: ([A-Z\-\s]+)", str(text))
            .group(1)
            .rstrip("A")
            .strip()
        )
    except:
        return ""


def getAppealTo(text):
    try:
        return re.search(r"Appeal To: (\w?) Appeal", str(text)).group(1).strip()
    except:
        return ""


def getLowerCourtAppealDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"[\n\s:\-]",
                "",
                re.search(
                    r"LowerCourt Appeal Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)
                ).group(1),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getDispositionDateOfAppeal(text):
    try:
        return datetime.strptime(
            re.sub(
                r"[\n\s:\-]",
                "",
                re.search(
                    r"Disposition Date Of Appeal: (\d\d?/\d\d?/\d\d\d\d)", str(text)
                ).group(1),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getDispositionTypeOfAppeal(text):
    try:
        return re.sub(
            r"[\n\s:\-]",
            "",
            re.search(r"Disposition Type Of Appeal: [^A-Za-z]+", str(text)).group(1),
        ).strip()
    except:
        return ""


def getAppealCaseNumber(text):
    try:
        return re.search(r"Appeal Case Number: (.+)", str(text)).group(1).strip()
    except:
        return ""


def getTransferReason(text):
    try:
        return re.search(r"Transfer Reason (.+)").group(1).strip()
    except:
        return ""


def getAdminLastUpdate(text):
    try:
        return datetime.strptime(
            re.search(
                r"(?s)Administrative Information.+?Last Update: (\d\d?/\d\d?/\d\d\d\d)",
                str(text),
            )
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getNumberOfSubpoenas(text):
    try:
        return int(
            re.sub(
                r"[\n\s:\-]",
                "",
                re.search(r"Number of Subponeas: (\d{3})", str(text)).group(1),
            ).strip()
        )
    except:
        return ""


def getAdminUpdatedBy(text):
    try:
        return re.search(r"Updated By: (\w{3})", str(text)).group(1).strip()
    except:
        return ""


def getTransferToAdminDocDate(text):
    try:
        return datetime.strptime(
            re.search(r"Transfer to Admin Doc Date: (\d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getTransferDesc(text):
    try:
        return (
            re.search(r"Transfer Desc: ([A-Z\s]{0,15} \d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(1)
            .strip()
        )
    except:
        return ""


def getContinuanceDate(text):
    try:
        return datetime.strptime(
            re.search(r"(?s)Continuance Date\s*\n*\s*(\d\d/\d\d/\d\d\d\d)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getContinuanceReason(text):
    try:
        return re.search(
            r"Continuance Reason\s*\n*\s*([A-Z0-9]{2}/[A-Z0-9]{2}/[A-Z0-9]{4})",
            str(text),
        ).group(1)
    except:
        return None


def getContinuanceDescription(text):
    try:
        return re.search(
            r"Description:(.+?)Number of Previous Continuances:", str(text)
        ).strip()
    except:
        return None


def getNumberOfPreviousContinuances(text):
    try:
        return int(
            re.search(
                r"Number of Previous Continuances:\s*\n*\s(\d+)", str(text)
            ).group(1)
        )
    except:
        return None


def getTBNV1(text):
    try:
        return datetime.strptime(
            re.search(r"Date Trial Began but No Verdict \(TBNV1\): ([^\n]+)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getTBNV2(text):
    try:
        return datetime.strptime(
            re.search(r"Date Trial Began but No Verdict \(TBNV2\): ([^\n]+)", str(text))
            .group(1)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getTurnOverDate(text):
    try:
        return datetime.strptime(
            re.search(r"TurnOver Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getTurnOverAmt(text):
    try:
        return float(re.search(r"TurnOver Amt\: \$(\d+\.\d\d)", str(text)).group(1))
    except:
        return ""


def getFrequencyAmt(text):
    try:
        return float(re.search(r"Frequency Amt\: \$(\d+\.\d\d)", str(text)).group(1))
    except:
        return ""


def getDueDate(text):
    try:
        return datetime.strptime(
            re.search(r"Due Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getOverUnderPaid(text):
    try:
        return float(re.search(r"Over/Under Paid: \$(\d+.\d\d)", str(text)).group(1))
    except:
        return None


def getEnforcementComments(text):
    try:
        return re.sub(
            r"(?s)Warrant Mailer.+",
            "",
            re.search(r"(?s)Comments: (.+?)\n Over/Under Paid", str(text))
            .group(1)
            .strip(),
        )
    except:
        return None


def getLastPaidDate(text):
    try:
        return datetime.strptime(
            re.search(r"Last Paid Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getPayor(text):
    try:
        return re.search(r"Payor\: ([A-Z0-9]{4})", str(text)).group(1)
    except:
        return ""


def getEnforcementStatus(text):
    try:
        return re.sub(
            r"F$",
            "",
            re.search(r"Enforcement Status\: ([A-Z\:,\s]+)", str(text)).group(1),
        ).strip()
    except:
        return ""


def getFrequency(text):
    try:
        return re.sub(
            r"Cost Paid By\:", "", re.search(r"Frequency\: ([W|M])", str(text)).group(1)
        )
    except:
        return ""


def getPlacementStatus(text):
    try:
        return re.search(r"Placement Status\: (.+)", str(text)).group(1).strip()
    except:
        return ""


def getPreTrial(text):
    try:
        return re.search(r"PreTrial\: (YES|NO)", str(text)).group(1)
    except:
        return ""


def getPreTrialDate(text):
    try:
        return datetime.strptime(
            re.search(r"PreTrail Date\: (.+)PreTrial", str(text)).group(1).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getPreTrialTerms(text):
    try:
        return re.search(r"PreTrial Terms\: (YES|NO)", str(text)).group(1)
    except:
        return ""


def getPreTermsDate(text):
    try:
        return datetime.strptime(
            re.search(r"Pre Terms Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getDelinquent(text):
    try:
        return re.search(r"Delinquent\: (YES|NO)", str(text)).group(1)
    except:
        return ""


def getDelinquentDate(text):
    try:
        return datetime.strptime(
            re.search(r"Delinquent Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getDAMailer(text):
    try:
        return re.search(r"DA Mailer\: (YES|NO)", str(text)).group(1)
    except:
        return ""


def getDAMailerDate(text):
    try:
        return datetime.strptime(
            re.search(r"DA Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getWarrantMailer(text):
    try:
        return re.search(r"Warrant Mailer\: (YES|NO)", str(text)).group(1)
    except:
        return ""


def getWarrantMailerDate(text):
    try:
        return datetime.strptime(
            re.search(r"Warrant Mailer Date\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(
                1
            ),
            "%m/%d/%Y",
        )
    except:
        return None


def getLastUpdate(text):
    try:
        return re.search(r"Last Update\: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1)
    except:
        return ""


def getUpdatedBy(text):
    try:
        return re.search(r"Updated By\: ([A-Z]{3})", str(text)).group(1)
    except:
        return ""


def getSentencingRequirementsCompleted(text):
    try:
        return re.sub(
            r"[\n:]|Requrements Completed",
            "",
            ", ".join(re.findall(r"(?:Requrements Completed: )([YES|NO]?)", str(text))),
        )
    except:
        return ""


def getSentenceDate(text):
    try:
        return datetime.strptime(
            re.search(r"(Sentence Date: )(\d\d?/\d\d?/\d\d\d\d)", str(text))
            .group(2)
            .strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getJailCreditPeriod(text):
    try:
        return "".join(
            re.search(r"Days\.\s*(\d+ Years, \d+ Months, \d+ Days\.)\s+", str(text))
            .group(1)
            .strip()
        )
    except:
        return ""


def getSentenceProvisions(text):
    try:
        return re.search(r"Sentence Provisions: ([Y|N]?)", str(text)).group(1).strip()
    except:
        return ""


def getSentenceStartDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"(Sentence Start Date:)",
                "",
                ", ".join(
                    re.findall(
                        r"Sentence Start Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)
                    )
                ),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getSentenceEndDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"(Sentence End Date:)",
                "",
                ", ".join(
                    re.findall(r"Sentence End Date: (\d\d?/\d\d?/\d\d\d\d)", str(text))
                ),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getProbationBeginDate(text):
    try:
        return datetime.strptime(
            re.sub(
                r"(Probation Begin Date:)",
                "",
                ", ".join(
                    re.findall(
                        r"Probation Begin Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)
                    )
                ),
            ).strip(),
            "%m/%d/%Y",
        )
    except:
        return None


def getProbationPeriod(text):
    try:
        return re.search(
            r"Probation Period\: (\d+ Years, \d+ Months, \d+ Days\.)", str(text)
        ).group(1)
    except:
        return ""


def getLicenseSuspPeriod(text):
    try:
        return re.search(
            r"License Susp Period\: (\d+ Years, \d+ Months, \d+ Days\.)", str(text)
        ).group(1)
    except:
        return ""


def getProbationRevoke(text):
    try:
        return re.sub(
            r"(Probation Revoke:)",
            "",
            ", ".join(
                re.findall(r"Probation Revoke: (\d\d?/\d\d?/\d\d\d\d)", str(text))
            ),
        ).strip()
    except:
        return ""


def getAttorneys(text):
    att = re.search(
        r"(Type of Counsel Name Phone Email Attorney Code)(.+)(Warrant Issuance)",
        str(text),
        re.DOTALL,
    )
    if att:
        att = att.group(2)
        return re.sub(r"Warrant.+", "", att, re.DOTALL).strip()
    else:
        return ""


def getCaseActionSummary(text):
    cas = re.search(
        r"(Case Action Summary)([^\\]*)(Images\s+?Pages)", str(text), re.DOTALL
    )
    if cas:
        cas = cas.group(2)
        return re.sub(
            r"© Alacourt\.com|Date: Description Doc# Title|Operator", "", cas, re.DOTALL
        ).strip()
    else:
        return ""


def getImages(text):
    imgs = re.findall(
        r"(Images\s+?Pages)([^\\n]*)(END OF THE REPORT)", str(text), re.DOTALL
    )
    if len(imgs) > 1:
        imgs = "; ".join(imgs).strip()
    elif len(imgs) == 1:
        return imgs[0][1].strip()
    else:
        return ""


def getWitnesses(text):
    wit = re.search(r"(Witness.+?Case Action Summary)", str(text), re.DOTALL)
    if wit:
        wit = wit.group()
        wit = re.sub(r"© Alacourt.com \d\d?/\d\d?/\d\d\d\d", "", wit, re.DOTALL)
        wit = re.sub(r"Witness", "", wit, re.DOTALL)
        wit = re.sub(r"\#Name", "", wit, re.DOTALL)
        wit = re.sub(r"Date", "", wit, re.DOTALL)
        wit = re.sub(r"Served", "", wit, re.DOTALL)
        wit = re.sub(r"Service", "", wit, re.DOTALL)
        wit = re.sub(r"Type", "", wit, re.DOTALL)
        wit = re.sub(r"Attorney", "", wit, re.DOTALL)
        wit = re.sub(r"Issued", "", wit, re.DOTALL)
        wit = re.sub(r"Type", "", wit, re.DOTALL)
        wit = re.sub(r"SJIS", "", wit, re.DOTALL)
        wit = re.sub(r"Witness", "", wit, re.DOTALL)
        wit = re.sub(r"List", "", wit, re.DOTALL)
        wit = re.sub(r"Date Issued", "", wit, re.DOTALL)
        wit = re.sub(r"Subpoena", "", wit, re.DOTALL)
        wit = re.sub(r"Date\:", "", wit, re.DOTALL)
        wit = re.sub(r"Time", "", wit, re.DOTALL)
        wit = re.sub(r"Code", "", wit, re.DOTALL)
        wit = re.sub(r"Comments", "", wit, re.DOTALL)
        wit = re.sub(r"Case Action Summary", "", wit, re.DOTALL)
        wit = re.sub(r"\:$", "", wit.strip(), re.DOTALL)
        return wit.strip()
    else:
        return ""


def getSettings(text):
    settings = re.search(r"(Settings.+?Court Action)", str(text), re.DOTALL)
    if settings:
        out = settings.group(1)
        out = re.sub(r"Settings", "", out, re.DOTALL)
        out = re.sub(r"Date\:", "", out, re.DOTALL)
        out = re.sub(r"Que\:", "", out, re.DOTALL)
        out = re.sub(r"Time\:", "", out, re.DOTALL)
        out = re.sub(r"Description\:", "", out, re.DOTALL)
        out = re.sub(r"Court Action", "", out, re.DOTALL)
        return out.strip()
    else:
        return ""


def getBalanceByFeeCode(text, code):
    pat = f"(ACTIVE[^\n]+{code}[^\n]+)"
    rows = re.findall(pat, text)
    tot = 0.0
    for r in rows:
        splr = re.findall(r"\$\d+\.\d{2}", r)
        if len(splr) > 0:
            bal = float(re.sub(r"\$", "", splr[-1]))
            tot += bal
    if len(rows) == 0:
        return None
    if len(rows) > 0:
        return tot


def getAmtDueByFeeCode(text, code):
    pat = f"(ACTIVE[^\n]+{code}[^\n]+)"
    rows = re.findall(pat, text)
    tot = 0.0
    for r in rows:
        splr = re.findall(r"\$\d+\.\d{2}", r)
        if len(splr) > 0:
            bal = float(re.sub(r"\$", "", splr[0]))
            tot += bal
    if len(rows) == 0:
        return None
    if len(rows) > 0:
        return tot


def getAmtPaidByFeeCode(text, code):
    pat = f"(ACTIVE[^\n]+{code}[^\n]+)"
    rows = re.findall(pat, text)
    tot = 0.0
    for r in rows:
        splr = re.findall(r"\$\d+\.\d{2}", r)
        if len(splr) > 0:
            bal = float(re.sub(r"\$", "", splr[1]))
            tot += bal
    if len(rows) == 0:
        return None
    if len(rows) > 0:
        return tot


def getAmtHoldByFeeCode(text, code):
    pat = f"(ACTIVE[^\n]+{code}[^\n]+)"
    rows = re.findall(pat, text)
    tot = 0.0
    for r in rows:
        splr = re.findall(r"\$\d+\.\d{2}", r)
        if len(splr) > 0:
            bal = float(re.sub(r"\$", "", splr[2]))
            tot += bal
    if len(rows) == 0:
        return None
    if len(rows) > 0:
        return tot


def getSuspensionDate(text):
    try:
        return datetime.strptime(
            re.search(r"Suspension Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getSpeed(text):
    try:
        return int(re.search(r"Speed: (\d+)", str(text)).group(1))
    except:
        return None


def getCompletionDate(text):
    try:
        return datetime.strptime(
            re.search(r"Completion Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getClearDate(text):
    try:
        return datetime.strptime(
            re.search(r"Clear Date: (\d\d?/\d\d?/\d\d\d\d)", str(text)).group(1),
            "%m/%d/%Y",
        )
    except:
        return None


def getSpeedLimit(text):
    try:
        return int(re.search(r"Speed Limit: (\d+)", str(text)).group(1))
    except:
        return None


def getBloodAlcoholContent(text):
    try:
        return float(
            re.search(
                r"Blood Alcohol Content: Completion Date: ?(\d\d?/\d\d?/\d\d\d\d)? (\d+\.\d\d\d)",
                str(text),
            ).group(2)
        )
    except:
        return None


def getTicketNumber(text):
    try:
        return re.search(r"Ticket Number: (.+)", str(text)).group(1).strip()
    except:
        return ""


def getRule20(text):
    try:
        return re.search(r"Rule 20: (.+?) Clear Date:").group(1).strip()
    except:
        return ""


def getCollectionStatus(text):
    try:
        return re.sub(
            r"\s+",
            " ",
            re.sub(
                r"\n",
                "",
                re.search(
                    r"(?s)Collection Status: (.+?) \d\d?/\d\d?/\d\d\d\d", str(text)
                ).group(1),
            ),
        ).strip()
    except:
        return ""


def getVehicleDesc(text):
    try:
        return re.search(r"Tag Number: (.+?) Vehicle Desc:", str(text)).group(1).strip()
    except:
        return ""


def getVehicleState(text):
    try:
        return int(re.search(r"Vehicle State: (\d+)", str(text)).group(1).strip())
    except:
        return None


def getDriverLicenseClass(text):
    try:
        return re.sub(
            r"/.+", "", re.search(r"Driver License Class: (.+)", str(text)).group(1)
        ).strip()
    except:
        return ""


def getCommercialVehicle(text):
    try:
        return re.search(r"Commercial Vehicle: (YES|NO|UNKNOWN)", str(text)).group(1)
    except:
        return ""


def getTagNumber(text):
    try:
        return re.search(r"([A-Z0-9]+) Tag Number:", str(text)).group(1)
    except:
        return ""


def getVehicleYear(text):
    try:
        return (
            re.search(r"Vehicle Year: (.+?) ?Vehicle State:", str(text))
            .group(1)
            .strip()
        )
    except:
        return ""


def getPassengersPresent(text):
    try:
        return re.search(r"(YES|NO) Passengers Present:", str(text)).group(1)
    except:
        return ""


def getCommercialDriverLicenseRequired(text):
    try:
        return re.search(
            r"Commercial Driver License Required: (YES|NO)", str(text)
        ).group(1)
    except:
        return ""


def getHazardousMaterials(text):
    try:
        return re.search(r"Hazardous Materials: (YES|NO)", str(text)).group(1)
    except:
        return ""
