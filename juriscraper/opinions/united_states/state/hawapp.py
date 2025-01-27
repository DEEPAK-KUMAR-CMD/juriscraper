# Author: Michael Lissner
# Date created: 2013-05-23


from juriscraper.opinions.united_states.state import haw


class Site(haw.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_code = "ICA"

    def get_court_name(self):
        return "Intermediate Court of Appeals"

    def get_class_name(self):
        return "hawapp"
