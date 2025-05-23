"""
Contact: Sara Velasquez, svelasquez@idcourts.net, 208-947-7501
History:
 - 2014-08-05, mlr: Updated.
 - 2015-06-19, mlr: Updated to simply the XPath expressions and to fix an OB1
   problem that was causing an InsanityError. The cause was nasty HTML in their
   page.
 - 2015-10-20, mlr: Updated due to new page in use.
 - 2015-10-23, mlr: Updated to handle annoying situation.
 - 2016-02-25 arderyp: Updated to catch "ORDER" (in addition to "Order") in download url text
"""
from datetime import datetime
import \
    re

from lxml import html

from casemine.casemine_util import CasemineUtil
from juriscraper.lib.string_utils import clean_if_py3, convert_date_string
from juriscraper.OpinionSite import OpinionSite


class Site(OpinionSite):
    # Skip first row of table, it's a header
    path_table_row_start = "//table//tr[position() > 1]"
    # Skip rows that don't have  link in 4th cell with
    # either 'Opinion', 'Order', 'ORDER', or 'Amend' in
    # the link text
    path_conditional_anchor = (
        "a["
        'contains(.//text(), "Opinion") or '
        'contains(.//text(), "Order") or '
        'contains(.//text(), "ORDER") or '
        'contains(.//text(), "Amended")'
        "]"
    )
    path_conditional_row = f"/td[4]//{path_conditional_anchor}"
    path_base = f"{path_table_row_start}[./{path_conditional_row}]"
    ctr=0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://www.isc.idaho.gov/appeals-court/isc_civil"
        self.court_id = self.__module__

    def _get_case_names(self):
        case_names = []
        path = f"{self.path_base}/td[3]"
        custom_ctr=0
        for cell in self.html.xpath(path):
            if custom_ctr==self.ctr:
                break
            name_string = html.tostring(
                cell, method="text", encoding="unicode"
            )
            name_string = clean_if_py3(name_string).strip()
            if name_string:
                case_names.append(name_string)
            custom_ctr+=1
        return case_names

    def _get_download_urls(self):
        # We'll accept an order document if the opinion document
        # is missing. But we obviously prefer the opinion doc,
        # as indicated in the algorithm below. Since each row
        # can list multiple valid links, we will parse all
        # acceptable links, take the opinion link if present,
        # otherwise take the first acceptable link.
        opinion_urls = []
        path = f"{self.path_base}/td[4]"
        path_link = f".//{self.path_conditional_anchor}"
        custom_ctr = 0
        for cell in self.html.xpath(path):
            if custom_ctr==self.ctr:
                break
            urls = []
            url_opinion = False
            for link in cell.xpath(path_link):
                text = link.text_content().strip()
                url = link.attrib["href"].replace("http://", "https://")
                urls.append(url)
                if "Opinion" in text:
                    url_opinion = url
            opinion_urls.append(url_opinion if url_opinion else urls[0])
            custom_ctr+=1
        return opinion_urls

    def _get_case_dates(self):
        case_dates = []
        path = f"{self.path_base}/td[1]"
        for cell in self.html.xpath(path):
            date_string = html.tostring(
                cell, method="text", encoding="unicode"
            )
            date_string = clean_if_py3(date_string).strip()
            if date_string:
                date_string = date_string.replace("Sept ", "Sep ").replace(".","")
                match = re.match(r"([A-Za-z]{3}) (\d{1,2}), (\d{4})", date_string)
                date_obj=''
                if match:
                    date_obj=datetime.strptime(match.group(),"%b %d, %Y").strftime("%d/%m/%Y")
                else:
                    date_obj = datetime.strptime(date_string, "%B %d, %Y").strftime("%d/%m/%Y")

                res=CasemineUtil.compare_date(self.crawled_till,date_obj)
                if res==1:
                    break
                case_dates.append(convert_date_string(date_string))
                self.ctr+=1
        return case_dates

    def _get_docket_numbers(self):
        doc=[]
        # print(self.ctr)
        path = f"{self.path_base}/td[2]//text()"
        custom_ctr=0
        for text in self.html.xpath(path):
            if custom_ctr==self.ctr:
                break
            text=str(text).strip()
            if text:
                doc_arr=[]
                if text.__contains__("/"):
                    doc_arr=text.replace(" ","").split('/')
                elif text.__contains__("&"):
                    doc_arr=text.replace(" ","").split('&')
                else:
                    doc_arr.append(text)
                doc.append(doc_arr)
                custom_ctr+=1
        return doc

    def _get_precedential_statuses(self):
        return ["Published"] * self.ctr

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        self.parse()
        return 0

    def get_class_name(self):
        return "idaho_civil"

    def get_court_name(self):
        return "Supreme Court of Idaho"

    def get_court_type(self):
        return "state"

    def get_state_name(self):
        return "Idaho"