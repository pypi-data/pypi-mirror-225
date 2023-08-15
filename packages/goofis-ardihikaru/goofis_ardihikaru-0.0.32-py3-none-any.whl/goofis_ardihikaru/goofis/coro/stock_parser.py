from abc import ABC
from typing import List

import requests
from parsel import Selector
from requests import Response

from goofis_ardihikaru.dto.stock_data import StockData
from goofis_ardihikaru.goofis.coro.abc import AbcParser
from goofis_ardihikaru.utils.currency import clean_currency, get_price_ranges, get_price_with_unit, \
    get_percent_value, \
    get_financial_value
from goofis_ardihikaru.utils.user_agent import build_fake_ua
from goofis_ardihikaru.utils.my_html_parser import MyHTMLParser


class StockParser(AbcParser, ABC):
    def __init__(self, code: str, lang: str, timeout: int = 30):
        super().__init__(code, lang)
        self.timeout = timeout
        self.url = f"https://www.google.com/finance/quote/{code}?hl={lang}"

        self.headers = {
            "User-Agent": build_fake_ua()
        }

        self.i = 0
        self.j = 0
        self.info = StockData()

    async def get(self):
        html = await self.get_html()

        return await self.parser(html)

    async def get_html(self):
        return requests.get(self.url, headers=self.headers, timeout=self.timeout)

    async def contains_day_range(self, general_info_list: List) -> bool:
        # when this value and next value contains '-' symbol
        this_val = general_info_list[self.i]
        next_val = general_info_list[(self.i + 1)]

        if "-" in this_val and "-" in next_val:
            return True

        return False

    async def contains_ceo_row(self, general_info_list: List) -> bool:
        """
            checks if ceo row exists or not

            sample with missing ceo row: ACES:IDX
        """
        # when this value and next value contains '-' symbol
        expected_year_val = general_info_list[self.i][-4:]

        try:
            _ = int(expected_year_val)
            return False
        except ValueError:
            return True

    def contains_head_office(self, general_info_list: List) -> bool:
        """
            checks if "kantor pusat" row exists or not

            sample with "kantor pusat" row: ASGR:IDX
        """
        # when this value and next value contains '-' symbol
        val = general_info_list[self.i]

        if "Indonesia" in val:
            return True
        else:
            return False

    def contains_average_volume(self, general_info_list: List) -> bool:
        """
            checks if "average volume" row exists or not

            sample with "average volume" row: BPII:IDX
        """
        # when this value and next value contains '-' symbol
        expected_exchange_val = general_info_list[self.i + 2]

        if expected_exchange_val != "IDX":
            return True
        else:
            return False

    async def update_general_info(self, general_info_list: List):
        """ updates general information """
        self.i = 0

        self.info.general.prev_price_close = clean_currency(general_info_list[self.incr()], self.lang)
        if await self.contains_day_range(general_info_list):
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

        # if total list only 7, there is no market cap!
        if len(general_info_list) > 7:
            (self.info.general.market_cap, self.info.general.market_cap_unit) = get_price_with_unit(
                general_info_list[self.incr()], self.lang,
            )

        if self.contains_average_volume(general_info_list):
            (self.info.general.avg_volume, self.info.general.avg_volume_unit) = get_price_with_unit(
                general_info_list[self.incr()], self.lang,
            )

        self.info.general.pe_ratio = clean_currency(general_info_list[self.incr()], self.lang)
        self.info.general.dividend_yield = get_percent_value(general_info_list[self.incr()], self.lang)
        self.info.general.primary_exchange = general_info_list[self.incr()]

        # if total list only 7, there is no extra information!
        if len(general_info_list) > 7:
            if await self.contains_ceo_row(general_info_list):
                ceo: str = general_info_list[self.incr()]
                ceo = ceo.replace("'", "")
                self.info.general.ceo = ceo

            # some stocks may only has year, such as, ACES:IDX
            self.info.general.founded_at = general_info_list[self.incr()]

            if self.contains_head_office(general_info_list):
                self.info.general.head_office = general_info_list[self.incr()]

            self.info.general.website = general_info_list[self.incr()]
            self.info.general.employees = clean_currency(general_info_list[self.incr()], self.lang)

    async def update_income_statement(self, financial_info_list: List, financial_percent_data_list: List):
        # quarter data
        self.info.financial.quarter.income_statement.revenue = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.operating_expense = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.net_income = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.net_income_margin = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.earning_per_share = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.ebitda = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.income_statement.effective_tax_rate = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )

    async def update_balance_sheet(self, financial_info_list: List, financial_percent_data_list: List):
        # quarter data
        self.info.financial.quarter.balance_sheet.cash_n_short_term_investment = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.total_assets = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.total_liabilities = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.total_equity = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.share_outstanding = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.price_to_book = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.return_on_assets = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.balance_sheet.return_on_capital = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )

    async def update_cash_flow(self, financial_info_list: List, financial_percent_data_list: List):
        # quarter data
        self.info.financial.quarter.cash_flow.net_income = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.cash_flow.cash_from_operation = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.cash_flow.cash_from_investing = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.cash_flow.cash_from_financing = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.cash_flow.net_change_in_cash = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )
        self.info.financial.quarter.cash_flow.free_cash_flow = get_financial_value(
            self.lang, financial_info_list[self.incr()], financial_percent_data_list[self.incr_j()]
        )

    async def update_financial_info(self, financial_info_list: List, financial_percent_data_list: List):
        """ updates financial information """
        self.i = 0
        self.j = 0

        if len(financial_info_list) > 0:
            # # balance_sheet
            await self.update_income_statement(financial_info_list, financial_percent_data_list)

            # # balance_sheet
            await self.update_balance_sheet(financial_info_list, financial_percent_data_list)

            # # cash_flow
            await self.update_cash_flow(financial_info_list, financial_percent_data_list)

    async def parser(self, html: Response):
        selector = Selector(text=html.text)

        general_info_list = await self.fetch_general_info(selector)
        await self.update_general_info(general_info_list)

        self.info.about = await self.fetch_about_info(selector)
        self.info.name = await self.fetch_name(selector, self.info.about, self.lang)
        self.info.current_price = await self.fetch_current_price(selector, self.lang)
        self.info.current_price_change_percent = await self.fetch_current_price_percent(selector, self.lang)
        self.info.current_price_change_value = await self.fetch_current_price_percent(selector, self.lang)

        financial_info_list, financial_percent_data_list = await self.fetch_financial_info(selector)
        await self.update_financial_info(financial_info_list, financial_percent_data_list)

        return self.info.to_dict()

    def incr(self) -> int:
        current_idx = self.i

        # do increment
        self.i += 1

        return current_idx

    def incr_j(self) -> int:
        current_idx = self.j

        # do increment
        self.j += 1

        return current_idx

    @staticmethod
    async def fetch_financial_info(selector: Selector) -> (list, list):
        financial_data = []
        for index, financials in enumerate(selector.css(".QXDnM"), start=0):
            val = financials.css("::text").get()
            financial_data.append(val)

        # data (%)
        financial_percent_data = []
        for index, financials in enumerate(selector.css(".gEUVJe"), start=0):
            val = financials.css("::text").get()
            financial_percent_data.append(val)

        return financial_data, financial_percent_data

    @staticmethod
    async def fetch_general_info(selector: Selector):
        # fetches data from the google finance
        general_info_list = []
        for index, data_results in enumerate(selector.css(".gyFHrc"), start=1):
            val = data_results.css(".P6K39c::text").get()

            # for website and head_office
            if val is None:
                data_with_link_selector = data_results.css(".P6K39c")
                sel = data_with_link_selector.css(".tBHE4e").get()

                parser = MyHTMLParser()
                parser.feed(sel)
                val = parser.content

            general_info_list.append(val)

        return general_info_list
