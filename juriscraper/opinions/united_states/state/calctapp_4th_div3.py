# Scraper for California's Fourth District Court of Appeal Division 3
# CourtID: calctapp_4th_div3
# Court Short Name: Cal. Ct. App.
from datetime import datetime

from juriscraper.opinions.united_states.state import calctapp_1st


class Site(calctapp_1st.Site):
    court_code = "G"
    division = "4th App. Dist. Div. 3"

    def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
        self.parse()
        return 0

    def get_class_name(self):
        return "calctapp_4th_div3"

    def get_court_name(self):
        return "California Court of Appeals"
