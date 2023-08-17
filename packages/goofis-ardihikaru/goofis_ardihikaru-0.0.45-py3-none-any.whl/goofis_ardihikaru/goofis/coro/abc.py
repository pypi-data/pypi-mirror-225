from abc import ABC, abstractmethod
from typing import Dict

import requests
from cssselect import ExpressionError
from goofis_ardihikaru.utils.async_class import AsyncClass
from goofis_ardihikaru.utils.currency import clean_currency, get_percent_value
from goofis_ardihikaru.utils.user_agent import build_fake_ua
from goofis_ardihikaru.utils.utils import reformat_name
from parsel import Selector
from requests import Response


class AbcParser(AsyncClass, ABC):
    def __init__(self, code: str, lang: str, timeout: int = 30, url: str = "https://www.google.com/finance/quote",
                 headers: Dict = None):
        super().__init__()
        if headers is None:
            headers = {"User-Agent": build_fake_ua()}
        self.lang = lang
        self.timeout = timeout
        self.url = f"{url}/{code}?hl={lang}"

        self.headers = headers
        if headers is None:
            self.headers = {
                "User-Agent": build_fake_ua()
            }

        # headers = {"User-Agent": "Mozilla/5.0"}

        self.i = 0
        self.j = 0
        self.info = None

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

    async def get_html_text(self) -> str:
        html = await self.get_html()

        return html.text

    async def get(self):
        html = await self.get_html()

        return await self.parser(html)

    async def get_html(self):
        cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
        # return requests.get(self.url, headers=self.headers, timeout=self.timeout, cookies={'CONSENT': 'YES+'})
        return requests.get(self.url, headers=self.headers, timeout=self.timeout, cookies=cookies)

    @abstractmethod
    async def parser(self, html: Response):
        pass

    @staticmethod
    async def fetch_current_price(selector: Selector, lang: str) -> float:
        """
        fetches current price
        """
        try:
            current_price_str = selector.css(".YMlKec.fxKbKc::text").get()
            return clean_currency(current_price_str, lang)
        except ExpressionError:
            return 0.0

    @staticmethod
    async def fetch_current_price_percent(selector: Selector, lang: str) -> float:
        """
        fetches current price
        """
        try:
            current_price_percent_str = selector.css(".JwB6zf::text").get()
            return get_percent_value(current_price_percent_str, lang)
        except ExpressionError:
            return 0.0

    async def fetch_current_price_percent_v2(self) -> float:
        """
        fetches current price percent changes
        """
        try:
            # current price
            current_price = self.info.current_price
            yesterday_price = self.info.general.prev_price_close

            diff = yesterday_price - current_price
            minus = 1
            if diff < -1:
                minus = -1

            # to percent
            diff_percent = diff / yesterday_price * 100
            diff_percent = round((diff_percent * minus), 2)

            return diff_percent
        except Exception:
            return 0.0

    @staticmethod
    async def fetch_current_price_value(last_closed_price: float, current_price: float) -> float:
        """
        fetches current price value
        """
        try:
            return round((last_closed_price - current_price), 2)
        except ExpressionError:
            return 0.0

    async def fetch_current_price_value_v2(self) -> float:
        """
        fetches current price changes
        """
        try:
            # current price
            current_price = self.info.current_price
            yesterday_price = self.info.general.prev_price_close

            diff = yesterday_price - current_price
            minus = 1
            if diff < -1:
                minus = -1
            diff = round((diff * minus), 2)

            return diff
        except Exception:
            return 0.0

    @staticmethod
    async def fetch_about_info(selector: Selector) -> str:
        """
        fetches `about company` information

        one example with missing `about company` data: BCIP:IDX
        """
        about = ""
        try:
            about = selector.css(".bLLb2d::text").get()
        except TypeError:
            pass
        except Exception:
            pass

        return about

    @staticmethod
    async def fetch_name(selector: Selector, about: str, lang: str) -> str:
        """
        fetches `name` information
        """
        name = ""
        try:
            name = selector.css(".zzDege::text").get()
            if name is None:
                raise TypeError("`name` is None")
        except TypeError:
            pass
        except Exception:
            pass

        # optional: casts value by collecting value from the `about company`
        name = reformat_name(name, about, lang)

        return name.strip()
