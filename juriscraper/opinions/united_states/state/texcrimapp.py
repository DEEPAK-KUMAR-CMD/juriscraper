# Scraper for Texas Criminal Court of Appeals
# CourtID: texcrimapp
# Court Short Name: TX
# Author: Michael Lissner
# Reviewer: None
# Date: 2015-09-02


from juriscraper.opinions.united_states.state import tex


class Site(tex.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_name = "ccrimapp"
        self.checkbox = 1

    def get_court_name(self):
        return "Texas Court of Criminal Appeals"

    def get_class_name(self):
        return "texcrimapp"
