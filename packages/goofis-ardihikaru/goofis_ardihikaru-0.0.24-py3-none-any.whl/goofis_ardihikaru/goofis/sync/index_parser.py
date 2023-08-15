from abc import ABC
from typing import List

from parsel import Selector
from requests import Response

from goofis_ardihikaru.dto.index_data import IndexData
from goofis_ardihikaru.goofis.sync.abc import AbcParser
from goofis_ardihikaru.utils.currency import clean_currency, get_price_ranges


class IndexParser(AbcParser, ABC):
    def __init__(self, code: str, lang: str, timeout: int = 30):
        super().__init__(code, lang, timeout)

        # override default value
        self.info = IndexData()

    def update_general_info(self, general_info_list: List):
        """ updates general information """

        self.info.general.prev_price_close = clean_currency(general_info_list[self.incr()], self.lang)
        (self.info.general.day_range_min, self.info.general.day_range_max,
         self.info.general.day_range_diff) = get_price_ranges(
            general_info_list[self.incr()], self.lang,
        )
        if self.info.general.day_range_diff > 0:
            self.info.general.day_range_increase = True

        (self.info.general.year_range_min, self.info.general.year_range_max,
         self.info.general.year_range_diff) = get_price_ranges(
            general_info_list[self.incr()], self.lang,
        )
        if self.info.general.year_range_diff > 0:
            self.info.general.year_range_increase = True

    # overriding abstract method
    def parser(self, html: Response):
        selector = Selector(text=html.text)

        general_info_list = self.fetch_general_info(selector)
        self.update_general_info(general_info_list)

        self.info.about = self.fetch_about_info(selector)
        self.info.name = self.fetch_name(selector, self.info.about, self.lang)
        self.info.current_price = self.fetch_current_price(selector, self.lang)
        self.info.current_price_change_percent = self.fetch_current_price_percent(selector, self.lang)
        self.info.current_price_change_value = self.fetch_current_price_value(
            self.info.general.prev_price_close, self.info.current_price
        )

        return self.info.to_dict()

    @staticmethod
    def fetch_general_info(selector: Selector):
        # fetches data from the google finance
        general_info_list = []
        for index, data_results in enumerate(selector.css(".gyFHrc"), start=1):
            val = data_results.css(".P6K39c::text").get()

            general_info_list.append(val)

        return general_info_list
