from juriscraper.opinions.united_states.federal_district import gov_info


class Site(gov_info.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_name = "United States Bankruptcy Court Southern District of Alabama"

    def get_class_name(self):
        return "bank_sd_ala"

    def get_court_type(self):
        return 'Bankruptcy'

    def get_state_name(self):
        return "11th Circuit"

    def get_court_name(self):
        return "Bankruptcy Court Southern District of Alabama"