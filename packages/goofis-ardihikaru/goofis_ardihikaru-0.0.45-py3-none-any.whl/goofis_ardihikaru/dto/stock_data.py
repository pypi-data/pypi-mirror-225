from dataclasses import dataclass, asdict
from typing import Dict, Union, Any

import simplejson as json

from goofis_ardihikaru.enums.price_change import ValueChange


@dataclass
class General:
    """ General Data model """

    prev_price_close: float = 0.0

    day_range_min: float = 0.0
    day_range_max: float = 0.0
    day_range_diff: float = 0.0
    day_range_increase: bool = False

    year_range_min: float = 0.0
    year_range_max: float = 0.0
    year_range_diff: float = 0.0
    year_range_increase: bool = False

    # 1 trillion (T) = 1,000 billions (B)
    market_cap: float = 0.0
    market_cap_unit: float = 0.0

    avg_volume: float = 0.0
    avg_volume_unit: float = 0.0

    pe_ratio: float = 0.0

    dividend_yield: float = 0.0
    primary_exchange: str = ""

    ceo: str = ""
    founded_at: str = ""
    website: str = ""
    head_office: str = ""
    employees: int = 0


@dataclass
class FinancialValue:
    """ Percentage Price Data model """

    unit: str = ""
    value: float = 0.0
    percent: float = 0.0
    price_change: str = ValueChange.NONE.value
    percent_change: str = ValueChange.NONE.value
    empty: bool = False
    empty_percent: bool = False


@dataclass
class IncomeStatement:
    """ Income Statement Data model """

    revenue: FinancialValue = FinancialValue()
    operating_expense: FinancialValue = FinancialValue()
    net_income: FinancialValue = FinancialValue()
    net_income_margin: FinancialValue = FinancialValue()
    earning_per_share: FinancialValue = FinancialValue()
    ebitda: FinancialValue = FinancialValue()
    effective_tax_rate: FinancialValue = FinancialValue()


@dataclass
class BalanceSheet:
    """ Balance Sheet Data model """

    cash_n_short_term_investment: FinancialValue = FinancialValue()
    total_assets: FinancialValue = FinancialValue()
    total_liabilities: FinancialValue = FinancialValue()
    total_equity: FinancialValue = FinancialValue()
    share_outstanding: FinancialValue = FinancialValue()
    price_to_book: FinancialValue = FinancialValue()
    return_on_assets: FinancialValue = FinancialValue()
    return_on_capital: FinancialValue = FinancialValue()


@dataclass
class CashFlow:
    """ Cash Flow Data model """

    net_income: FinancialValue = FinancialValue()
    cash_from_operation: FinancialValue = FinancialValue()
    cash_from_investing: FinancialValue = FinancialValue()
    cash_from_financing: FinancialValue = FinancialValue()
    net_change_in_cash: FinancialValue = FinancialValue()
    free_cash_flow: FinancialValue = FinancialValue()


@dataclass
class FinancialCategory:
    """ Financial Category Data model """

    income_statement: IncomeStatement = IncomeStatement()
    balance_sheet: BalanceSheet = BalanceSheet()
    cash_flow: CashFlow = CashFlow()


@dataclass
class Financial:
    """ Financial Data model """

    # quarter data
    quarter: FinancialCategory = FinancialCategory()

    # TODO: add annual data


@dataclass
class StockData:
    """ Stock data model """

    FN_ID = "id"
    FN_GENERAL = "general"
    FN_ABOUT = "about"
    FN_FINANCIAL = "financial"
    FN_CURRENT_PRICE = "current_price"
    FN_CURRENT_PRICE_CHANGE_PERCENT = "current_price_change_percent"
    FN_CURRENT_PRICE_CHANGE_VALUE = "current_price_change_value"

    id: str = "-1"
    general: General = General()
    financial: Financial = Financial()
    name: str = ""
    about: str = ""
    current_price: float = 0.0
    current_price_change_percent: float = 0.0
    current_price_change_value: float = 0.0

    @staticmethod
    def sanitize(val: str) -> str:
        """ sanitizes json string """
        val = val.replace("'", '"')
        val = val.replace("False", 'false')
        val = val.replace("True", 'true')

        return val

    def val_to_dict(self, val: Any) -> Union[None, int, str, Dict]:
        if val is None:
            return None
        if isinstance(val, int):
            return val
        if isinstance(val, str):
            return val

        val = str(val)

        # sanitizes
        val = self.sanitize(val)

        return json.loads(self.sanitize(val))

    def to_dict(self, with_id: bool = False):
        dict_data = asdict(self)

        # remove id if disabled
        if not with_id:
            dict_data.pop(self.FN_ID)

        return {
            k: self.val_to_dict(v) for k, v in dict_data.items()
        }
