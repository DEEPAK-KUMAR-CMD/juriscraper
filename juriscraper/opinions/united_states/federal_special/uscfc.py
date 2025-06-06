"""Scraper for the United States Court of Federal Claims
CourtID: uscfc
Court Short Name: Fed. Cl.

Notes:
    Scraper adapted for new website as of February 20, 2014.
"""

import datetime
import re

from lxml import html

from juriscraper.lib.exceptions import InsanityException
from juriscraper.lib.string_utils import (
    clean_if_py3,
    convert_date_string,
    titlecase,
)
from juriscraper.OpinionSite import OpinionSite


class Site(OpinionSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://www.uscfc.uscourts.gov/aggregator/sources/8"
        self.back_scrape_iterable = list(range(1, 4))
        self.court_id = self.__module__
        self.today = datetime.datetime.now()

    def _download(self, request_dict={}):
        if self.test_mode_enabled():
            # Use static 'today' date for consisting test results
            self.today = convert_date_string("2018/10/17")
        return super()._download(request_dict)

    def _get_case_dates(self):
        dates = []
        for item in self.html.xpath('//span[@class="feed-item-date"]'):
            text = item.text_content().strip()
            words = text.split()
            if len(words) == 2:
                date = convert_date_string(words[1])
            elif "ago" in text:
                # The record was added today "X hours and Y min ago"
                date = self.today
            else:
                raise InsanityException(
                    f"Unrecognized date element string: {text}"
                )
            dates.append(date)
        return dates

    def _get_case_names(self):
        case_names = []
        for t in self.html.xpath('//h3[@class="feed-item-title"]//text()'):
            t = " ".join(clean_if_py3(t).split())  # Normalize whitespace
            if t.strip():
                # If there is something other than whitespace...
                if not isinstance(t, str):
                    t = str(t, encoding="utf-8")

                if " • " in t:
                    t = t.split(" • ")[1].strip()
                t = titlecase(t.lower())
                case_names.append(t)
        return case_names

    def _get_download_urls(self):
        path = '//h3[@class="feed-item-title"]/a/@href'
        return list(self.html.xpath(path))

    def _get_precedential_statuses(self):
        return ["Published"] * len(self.case_names)

    def _get_docket_numbers(self):
        docket_numbers = []
        for t in self.html.xpath('//h3[@class="feed-item-title"]//text()'):
            t = clean_if_py3(t)
            if t.strip():
                # If there is something other than whitespace...
                if not isinstance(t, str):
                    t = str(t, encoding="utf-8")

                if " • " in t:
                    t = t.split(" • ")[0].strip()
                docket_numbers.append(t)
        return docket_numbers

    def _get_summaries(self):
        summaries = []
        path = '//div[@class="feed-item-body"]'
        for e in self.html.xpath(path):
            s = html.tostring(e, method="text", encoding="unicode")
            s = clean_if_py3(s).split("Keywords:")[0]
            summaries.append(s)

        return summaries

    def _get_judges(self):
        path = '//div[@class="feed-item-body"]'
        judges = []
        splitters = [
            "Signed by Chief Judge",
            "Signed by Judge",
            "Signed by Chief Special Master",  # Vaccine courts have odd names for judges
            "Signed by Special Master",
        ]
        for e in self.html.xpath(path):
            t = html.tostring(e, method="text", encoding="unicode")
            t = clean_if_py3(t).split("Keywords:")[0]
            for splitter in splitters:
                judge_parts = t.rsplit(splitter)
                if len(judge_parts) == 1:
                    # No splits found...
                    judge = ""
                    continue
                else:
                    judge = judge_parts[1]
                    break

            # Often the text looks like: 'Judge Susan G. Braden. (jt1) Copy to parties.' In that case we only
            # want the name, not the rest.
            length_of_match = 2
            m = re.search(
                r"[a-z]{%s}\." % length_of_match, judge
            )  # Two lower case letters followed by a period
            if m:
                judge = judge[: m.start() + length_of_match]
            else:
                judge = ""
            judge.strip(".")
            judges.append(judge)
        return judges

    def _download_backwards(self, page):
        self.url = (
            f"http://www.uscfc.uscourts.gov/aggregator/sources/8?page={page}"
        )
        self.html = self._download()

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        self._download_backwards(1)
        return 0

