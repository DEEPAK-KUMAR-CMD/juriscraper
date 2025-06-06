from datetime import datetime

from juriscraper.opinions.united_states.federal_appellate import (
    scotus_chambers,
)


class Site(scotus_chambers.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.precedential = "Relating-to"
        self.court = "relatingtoorders"

    # def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
    #     self.parse()
    #     return 0

    def get_class_name(self):
        return "scotus_relating"
