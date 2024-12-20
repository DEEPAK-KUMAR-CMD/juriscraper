from juriscraper.opinions.united_states.state import nj


class Site(nj.Site):
    days_interval = 45

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.base_url = self.url = (
            "https://www.njcourts.gov/attorneys/opinions/published-appellate"
        )
        self.status = "Published"

    def get_class_name(self):
        return "njsuperctappdiv_p"

    def get_court_name(self):
        return "Superior Court, Appellate Division"
