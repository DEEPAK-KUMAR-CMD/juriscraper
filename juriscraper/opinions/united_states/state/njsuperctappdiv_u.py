from juriscraper.opinions.united_states.state import njsuperctappdiv_p


class Site(njsuperctappdiv_p.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.base_url = self.url = (
            "https://www.njcourts.gov/attorneys/opinions/unpublished-appellate"
        )
        self.status = "Unpublished"

    def get_class_name(self):
        return "njsuperctappdiv_u"

    def get_court_name(self):
        return "Superior Court of New Jersey, Appellate Division"
