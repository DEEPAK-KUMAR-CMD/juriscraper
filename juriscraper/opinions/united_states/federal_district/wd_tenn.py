from juriscraper.opinions.united_states.federal_district import gov_info


class Site(gov_info.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_name = "United States District Court Western District of Tennessee"

    def get_class_name(self):
        return "wd_tenn"

    def get_court_type(self):
        return 'Federal'

    def get_state_name(self):
        return "6th Circuit"

    def get_court_name(self):
        return "Western District of Tennessee"
