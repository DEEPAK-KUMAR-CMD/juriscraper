"""This site is pretty bad. Very little HTML; everything is separated by
<br> tags. There is currently a case at the bottom of the page from 2009
that has incomplete meta data. You can see it in the example document.
"""
from juriscraper.opinions.united_states.federal_district import gov_info


class Site(gov_info.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.url = "http://www2.ca3.uscourts.gov/recentop/week/recprec.htm"
        self.court_id = self.__module__
        self.court_name = "United States Court of Appeals for the Third Circuit"

    def get_class_name(self):
        return "ca3_p"

    def get_court_type(self):
        return 'Federal'

    def get_state_name(self):
        return "3d Circuit"

    def get_court_name(self):
        return "Court of Appeals for the Third Circuit"

    # def _get_case_names(self):  #     return [  #         e  #         for e in self.html.xpath('//a[contains(@href, "opinarch")]/text()')  #     ]  #  # def _get_download_urls(self):  #     return [  #         e  #         for e in self.html.xpath('//a[contains(@href, "opinarch")]/@href')  #     ]  #  # def _get_case_dates(self):  #     dates = []  #     for text_string in self.html.xpath("//text()"):  #         if not text_string.lower().startswith("filed"):  #             continue  #         else:  #             date_string = text_string.split(" ")[1]  #             date_string = date_string.strip().strip(",")  #             date_object = datetime.strptime(date_string, '%m/%d/%Y')  #             date_filed = date_object.strftime('%d/%m/%Y')  #             res = CasemineUtil.compare_date(date_filed, self.crawled_till)  #             if res == 1:  #                 self.crawled_till = date_filed  #             dates.append(convert_date_string(date_string))  #     return dates  #  # def _get_docket_numbers(self):  #     docket_numbers = []  #     for text_string in self.html.xpath("//text()"):  #         if not text_string.lower().startswith("filed"):  #             continue  #         else:  #             docket= [text_string.split(" ")[3]]  #             docket_numbers.append(docket)  #     return docket_numbers  #  # def _get_precedential_statuses(self):  #     statuses = []  #     for _ in range(0, len(self.case_names)):  #         if "recprec" in self.url:  #             statuses.append("Published")  #         elif "recnonprec" in self.url:  #             statuses.append("Unpublished")  #         else:  #             statuses.append("Unknown")  #     return statuses  #  # def _get_lower_courts(self):  #     lower_courts = []  #     for e in self.html.xpath('//a[contains(@href, "opinarch")]'):  #         text_strings = e.xpath("./following-sibling::text()[1]")  #         text_string = " ".join(text_strings)  #         if (  #             text_string.lower().startswith("filed")  #             or text_string.strip() == ""  #         ):  #             lower_courts.append("Unknown")  #         else:  #             lower_courts.append(text_string.strip())  #     return lower_courts  #  # def crawling_range(self, start_date: datetime, end_date: datetime) -> int:  #     self.parse()  #     return 0
