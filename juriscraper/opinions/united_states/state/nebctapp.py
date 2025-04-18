from juriscraper.opinions.united_states.state import neb


class Site(neb.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = (
            "https://supremecourt.nebraska.gov/courts/court-appeals/opinions"
        )

    def get_class_name(self):
        return "nebctapp"

    def get_court_name(self):
        return "Nebraska Court of Appeals"

