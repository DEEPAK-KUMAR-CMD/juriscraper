"""
Court Contact: https://www.supremecourt.gov/contact/contact_webmaster.aspx
"""

from datetime import date, datetime
from typing import Dict, List, Union

from casemine.casemine_util import CasemineUtil
from juriscraper.AbstractSite import logger
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class Site(OpinionSiteLinear):
    justices = {
        "A": "Samuel Alito",
        "AB": "Amy Coney Barrett",
        "AS": "Antonin Scalia",
        "B": "Stephen Breyer",
        "BK": "Brett Kavanaugh",
        "D": "Decree",
        "DS": "David Souter",
        "EK": "Elana Kagan",
        "G": "Ruth Bader Ginsburg",
        "JS": "John Paul Stephens",
        "K": "Anthony Kennedy",
        "KJ": "Ketanji Brown Jackson",
        "NG": "Neil Gorsuch",
        "PC": "Per Curiam",
        "R": "John G. Roberts",
        "SS": "Sonia Sotomayor",
        "T": "Clarence Thomas",
    }
    base_url = "https://www.supremecourt.gov/opinions/slipopinion"
    first_opinion_date = datetime(2018, 6, 25)
    days_interval = 365

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.status = "Published"
        self.url = f"{self.base_url}/{self.get_term()}"
        self.make_backscrape_iterable(kwargs)

    @staticmethod
    def get_term(
        date_of_interest: Union[date, datetime] = date.today()
    ) -> int:
        """The URLs for SCOTUS correspond to the term, not the calendar.

        The terms kick off on the first Monday of October, so we use October 1st
        as our cut off date.
        """
        term_cutoff = date(date_of_interest.year, 10, 1)
        if isinstance(date_of_interest, datetime):
            date_of_interest = date_of_interest.date()
        year = int(date_of_interest.strftime("%y"))
        # Return the previous year if we haven't reached the cutoff
        return year - 1 if date_of_interest < term_cutoff else year

    def _process_html(self):
        for row in self.html.xpath("//tr"):
            cells = row.xpath(".//td")
            if len(cells) != 6:
                continue
            _, date, docket, link, justice, citation = row.xpath(".//td")
            if not link.text_content():
                continue
            curr_date = datetime.strptime(date.text_content(), "%m/%d/%y").strftime("%d/%m/%Y")
            res = CasemineUtil.compare_date(self.crawled_till, curr_date)
            if res == 1:
                return
            self.cases.append(
                {
                    "citation": [citation.text_content()],
                    "date": date.text_content(),
                    "url": link.xpath(".//a/@href")[0],
                    "name": link.text_content(),
                    "docket": [docket.text_content()],
                    "judge": [self.justices[justice.text_content()]],
                }
            )

    def make_backscrape_iterable(self, kwargs: Dict) -> List[str]:
        """Use the default make_backscrape_iterable to parse input
        and create date objects. Then, use the dates to get the terms

        Note that the HTML slipopinion page exists only since term 17

        :return: a list of URLs
        """
        super().make_backscrape_iterable(kwargs)
        start = self.get_term(self.back_scrape_iterable[0][0])
        end = self.get_term(self.back_scrape_iterable[-1][1])
        if start == end:
            self.back_scrape_iterable = [f"{self.base_url}/{start}"]
        else:
            self.back_scrape_iterable = [
                f"{self.base_url}/{yy}" for yy in range(start, end)
            ]

    def _download_backwards(self, d: str):
        self.url = d
        logger.info("Backscraping %s", self.url)
        self.html = self._download()
        self._process_html()

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        self.parse()
        return 0

    def get_class_name(self):
        return "scotus_slip"

    def get_court_name(self):
        return 'U.S. Supreme Court'

    def get_court_type(self):
        return 'Federal'

    def get_state_name(self):
        return "U.S. Supreme Court"
