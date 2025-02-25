from juriscraper.opinions.united_states.federal_district import gov_info


class Site(gov_info.Site):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.court_id = self.__module__
        self.court_name = "United States Court of Appeals for the Fourth Circuit"

    def get_class_name(self):
        return "ca4"

    def get_court_type(self):
        return 'Federal'

    def get_state_name(self):
        return "4th Circuit"

    def get_court_name(self):
        return "Court of Appeals for the Fourth Circuit"

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.court_id = self.__module__
    #     self.json = {}
    #     self.interval = 14
    #     self.back_scrape_iterable = [
    #         i.date()
    #         for i in rrule(
    #             DAILY,
    #             interval=self.interval,  # Every interval days
    #             dtstart=date(2022, 1, 1),
    #             until=date(2022, 7, 1),
    #         )
    #     ]
    #
    # def _download(self, request_dict={}):
    #     if self.test_mode_enabled():
    #         with open(self.url) as file:
    #             self.json = json.load(file)
    #     else:
    #         self.json = (
    #             self.request["session"]
    #             .post(
    #                 self.url,
    #                 json=self.parameters,
    #             )
    #             .json()
    #         )
    #
    # def _process_html(self) -> None:
    #     """Process CA4 Opinions
    #
    #     :return: None
    #     """
    #     for row in self.json["resultSet"]:
    #         package_id = row["fieldMap"]["packageid"]
    #         docket = row["line1"].split()[0]
    #         date_str = row["line2"].split("day, ")[1].strip(".")
    #         url = f"https://www.govinfo.gov/content/pkg/{package_id}/pdf/{package_id}-0.pdf"
    #
    #         self.cases.append(
    #             {
    #                 "docket": docket,
    #                 "name": row["fieldMap"]["title"],
    #                 "url": url,
    #                 "date": date_str,
    #                 "status": "Unknown",
    #             }
    #         )
    #
    # def extract_from_text(self, scraped_text: str) -> Dict[str, Any]:
    #     """Pass scraped text into function and return precedential status
    #
    #     :param scraped_text: Text of scraped content
    #     :return: metadata
    #     """
    #     if re.findall(r"\bPUBLISHED\b", scraped_text):
    #         status = "Published"
    #     elif re.findall(r"\bUNPUBLISHED\b", scraped_text):
    #         status = "Unpublished"
    #     else:
    #         status = "Unknown"
    #     metadata = {
    #         "OpinionCluster": {
    #             "precedential_status": status,
    #         },
    #     }
    #     return metadata
    #
    # def _download_backwards(self, dt) -> None:
    #     """Download backward over time method
    #
    #     :param dt: Datetime object
    #     :return: None
    #     """
    #     start = (dt - timedelta(days=7)).strftime("%Y-%m-%d")
    #     end = dt.strftime("%Y-%m-%d")
    #     self.parameters["query"] = f"publishdate:range({start},{end})"
    #     self.html = self._download()
    #
    # def crawling_range(self, start_date: datetime, end_date: datetime) -> int:
    #     self.url = "https://www.govinfo.gov/wssearch/search"
    #     today = end_date.strftime("%Y-%m-%d")
    #     last_month = start_date.strftime("%Y-%m-%d")
    #     self.parameters = {"facets": {"accodenav": ["USCOURTS", ],
    #         "governmentauthornav": [
    #             "United States Court of Appeals for the Fourth Circuit", ], },
    #         "filterOrder": ["accodenav", "governmentauthornav", ],
    #         "facetToExpand": "governmentauthornav", "offset": 0,
    #         "pageSize": "100", "sortBy": "2",
    #         "query": f"publishdate:range({last_month},{today})",
    #         "browseByDate": True, "historical": False, }
    #     self.method = "POST"
    #     self.parse()
    #     return 0
