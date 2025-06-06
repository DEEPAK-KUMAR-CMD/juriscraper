"""Scraper for the United States Court of Appeals for Veterans Claims
CourtID: cavc
Court Short Name: Vet. App.
History:
 - 2012-06-07: Created by Brian Carver
 - 2014-08-06: Updated by mlr.
 - 2023-01-23: Update by William Palin
"""
from datetime import date, datetime
import html
import re
from typing import Any, Dict

from lxml import html

from casemine.casemine_util import CasemineUtil
from juriscraper.lib.string_utils import titlecase
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class Site(OpinionSiteLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://www.uscourts.cavc.gov/opinions.php"
        self.court_id = self.__module__
        # self.last_month = date.today() - datetime.timedelta(weeks=4)
        self.status = "Published"

    def _process_html(self):
        cases = self.html.xpath(".//tbody/tr/td/a/parent::td/parent::tr")
        for case in cases:
            date_text = case.xpath(".//td/text()")[1]
            # print(date_text)
            clean_date = datetime.strptime(date_text, "%d%b%y")
            curr_date =  clean_date.strftime("%d/%m/%Y")
            res = CasemineUtil.compare_date(self.crawled_till, curr_date)
            if res == 1:
                return
            self.cases.append({
                "url": case.xpath(".//a/@href")[0],
                "date": clean_date.strftime("%m/%d/%Y"),
                "docket": [case.xpath(".//a/text()")[0]],
                "name":  case.xpath(".//td/text()")[0]
            })
            # print(html.tostring(case,pretty_print=True).decode("utf-8"))


    def _process_html_old(self):
        """Process the CAVC website and collect new opinions

        :return: None
        """
        if self.test_mode_enabled():
            self.last_month = datetime.datetime(2022, 12, 27).date()
        cases = self.html.xpath(".//tbody/tr/td/a/parent::td/parent::tr")
        for case in cases:
            try:
                _, date = case.xpath(".//td/text()")
                clean_date = datetime.datetime.strptime(date, "%d%b%y")
                if self.last_month > clean_date.date():
                    break
                self.cases.append(
                    {
                        "url": case.xpath(".//a/@href")[0],
                        "date": clean_date.strftime("%m/%d/%Y"),
                        "docket": case.xpath(".//a/text()")[0],
                        "name": "Case name extracted from text",
                    }
                )
            except ValueError:
                # The table has a malformed row
                continue

    def extract_from_text(self, scraped_text: str) -> Dict[str, Any]:
        """Can we extract the case name and clean it up?

        This method is a bit ... ugly.  Mostly due to bad PDFs that occur
        not often. This means weird whitespacing that makes this the most
        efficient method for name extraction

        :param scraped_text: The content of the document downloaded
        :return: Metadata to be added to the case
        """
        keepers = []
        start = False
        for row in scraped_text.split("\n"):
            check_row = re.sub(r"\s", "", row.upper())
            if re.findall(r"NOS?\.?\d+-\d+", check_row):
                start = True
                continue
            if not start:
                continue
            if "SECRETARY" in row.upper() or "VETERANS AFFAIRS" in row.upper():
                break
            if "Before" in row:
                break
            if not row.strip():
                continue
            if "JR" not in row:
                keepers.append(row.split(",", 1)[0].strip())
            else:
                keepers.append(row[: row.index("JR.") + 3].strip())
        case_name = titlecase(" ".join(keepers))
        metadata = {
            "OpinionCluster": {
                "case_name": case_name,
            },
        }
        return metadata

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        self.parse()
        return 0

    def get_class_name(self):
        return "cavc"

    def get_court_type(self):
        return "Special"

    def get_state_name(self):
        return "Claims"

    def get_court_name(self):
        return "United States Court of Appeals for Veterans Claims"