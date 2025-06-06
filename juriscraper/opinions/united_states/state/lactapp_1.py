"""Scraper for Louisiana Court of Appeal, First Circuit
CourtID: lactapp_1
Court Short Name: La. Ct. App. 1st Cir.
Author: mmantel
History:
  2019-11-24: Created by mmantel
"""

import math
import re
from datetime import datetime
from casemine.casemine_util import CasemineUtil
from juriscraper.lib.html_utils import (get_row_column_links,
                                        get_row_column_text, )
from juriscraper.OpinionSiteLinear import OpinionSiteLinear


class Site(OpinionSiteLinear):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.back_scrape_iterable = self._generate_back_scrape_range()
        # The opinions page does not indicate whether a case is
        # published or unpublished. That is only found in the PDF.
        # (Unpublished cases have "Not Designated For Publication" on
        # the cover page.)
        self.status = "Unknown"
        self.cipher = "AES128-SHA"
        self.set_custom_adapter(self.cipher)

    def _process_html(self):
        rows = self.html.cssselect("#opinion_contentTable tbody tr")
        if rows is None:
            return
        for row in rows:
            self.cases.append({"date": get_row_column_text(row, 1),
                               "docket": [self._parse_docket_numbers(row)],
                               "name": get_row_column_text(row, 4),
                               "url": get_row_column_links(row, 3), })

    def _parse_docket_numbers(self, row):
        # Handle cases such as:
        # "2018CA1765<br>Rehearing<br>Application"
        #     => "2018CA1765"
        # "2018CA1742<br>Consolidated With<br>2018CA1743"
        #     => "2018CA1742, 2018CA1743"
        text = get_row_column_text(row, 2)
        case_numbers = re.findall("[0-9]{4}[A-Z]{2}[0-9]{4}", text)
        return ", ".join(case_numbers)

    def _generate_back_scrape_range(self):
        # This is a generator function, so this code won't run until a
        # caller begins iterating, which is necessary because
        # otherwise this would run during unit tests and trigger an
        # unwanted network request.
        last_page = self._get_last_page_number()

        yield from range(1, last_page + 1)

    def _get_last_page_number(self):
        # The link to the last page has an onclick like:
        # javascript:opinion_doPostBack('paging','','&opinionsort_field=sortdate&opinionsort_field_by=&opinionsort_field_type=&opinionsort_type=DESC&opinionpage_size=50&opinionp=395')
        # where 395 is the last page number.
        html = self._get_html_tree_by_url(self._base_url, {})
        el = html.cssselect("a[title=last]")[0]
        onclick = el.get("onclick")
        return int(re.findall(r"\d+", onclick)[-1])

    def _download_backwards(self, page):
        self.url = self._base_url + ("&opinionp=%d" % page)
        self.html = self._download()
        self._process_html()

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        crawl_till_str = start_date.strftime("%d/%m/%Y")
        self._page_size = 50
        page = 1
        flag = True
        self._base_url = f"https://www.la-fcca.org/opiniongrid/opinionpub.php?opinionpage_size={self._page_size}"
        self.url = self._base_url
        self.method = 'POST'
        while flag:
            self.parameters = {"opinionmode": "view",
                               "opinionsort_field": "sortdate",
                               "opinionsort_field_by": "",
                               "opinionsort_field_type": "",
                               "opinionsort_type": "DESC",
                               "opinionpage_size": str(self._page_size),
                               "opinionp": str(page)}
            self.parse()
            page = page + 1
            self.downloader_executed = False
            trs = self.html.xpath(
                "//table[@id='opinion_contentTable']//tbody//tr//td[1]//label")
            for tr in trs:
                opn_date_str = str(tr.text).replace(' ', '')
                opn_date = datetime.strptime(opn_date_str, '%m/%d/%Y')
                opn_date_str = opn_date.strftime('%d/%m/%Y')
                comp = CasemineUtil.compare_date(opn_date_str, crawl_till_str)
                if comp == -1:
                    flag = False
                    break
        return 0

    def get_class_name(self):
        return 'lactapp_1'

    def get_court_name(self):
        return 'Louisiana Court of Appeal'

    def get_court_type(self):
        return 'state'

    def get_state_name(self):
        return 'Louisiana'
