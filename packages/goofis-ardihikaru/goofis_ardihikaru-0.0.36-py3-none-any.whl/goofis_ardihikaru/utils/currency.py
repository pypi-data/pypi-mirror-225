from typing import List, Tuple

from goofis_ardihikaru.dto.stock_data import FinancialValue
from goofis_ardihikaru.enums.currency_unit import CurrencyUnit
from goofis_ardihikaru.enums.language import Language
from goofis_ardihikaru.enums.price_change import ValueChange


def clean_currency(currency: str, lang: str) -> float:
    if currency == "-":
        return 0.0

    # sometimes it contains a percent symbol
    currency = currency.replace("%", "")

    currency = currency.replace("Rp", "")

    # for Indonesian-based format (?hl=id)
    # WARNING: kalau indonesia (?hl=id), delimiter ribuan pakai titik!
    if lang == Language.INDONESIA.value:
        currency = currency.replace(".00", "")
        currency = currency.replace(".", "")
        currency = currency.replace(",", ".")
    else:
        currency = currency.replace(",00", "")
        currency = currency.replace(".", "")

    currency = currency.replace(" ", "")

    return float(currency)


def get_price_ranges(price_range: str, lang: str) -> Tuple[float, float, float]:
    # first, split
    price_range_arr: List = price_range.split(" - ")

    # then, captures the data
    price_min: float = clean_currency(price_range_arr[0], lang)
    price_max: float = clean_currency(price_range_arr[1], lang)
    price_diff: float = round((price_max - price_min), 2)

    return price_min, price_max, price_diff


def get_price_with_unit(price_with_unit: str, lang: str) -> Tuple[float, str]:
    # sanitize
    price_with_unit = price_with_unit.replace("\xa0", "")  # removes space

    if f" {CurrencyUnit.ID_JT.value}" in price_with_unit:
        price_with_unit = price_with_unit.replace(" jt", " jt")

    # first, split
    price_range_arr: List = price_with_unit.split(" ")

    # only capture price and remove the currency symbol
    price_str = price_range_arr[0]

    # extracts data
    # unit `jt` is only for lang=id (Indonesia)
    if CurrencyUnit.ID_JT.value in price_str or CurrencyUnit.ID_RB.value in price_str:
        market_cap_unit = price_str[-2:]
        price = clean_currency(price_str[:-2], lang)
    else:
        market_cap_unit = price_str[-1]
        price = clean_currency(price_str[:-1], lang)

    return price, market_cap_unit


def get_percent_value(percent_val: str, lang: str) -> float:
    if percent_val == "-" or percent_val == "—":
        return 0.0

    # only for lang=id (Indonesia)
    if lang == Language.INDONESIA.value:
        percent_val = percent_val.replace(".", "")
        percent_val = percent_val.replace(",", ".")

    percent_val = percent_val.replace("%", "")
    percent_val = percent_val.replace("+", "")

    return float(percent_val)


def contains_unit(val: str) -> bool:
    """
        checks if it contains unit (e.g. `B`, `T`, `M`) or not
    """
    last_char = val[-1]

    try:
        # if int found, it DOES not contain unit
        _ = int(last_char)
        return False
    except ValueError:
        return True


def get_financial_value(lang: str, value_str: str, percent_str: str) -> FinancialValue:
    # empty value, ignore it
    if value_str == "—" and percent_str == "—":
        return FinancialValue(empty=True)
    elif value_str == "∞" and percent_str == "—":
        return FinancialValue(empty=True)

    # extracts data
    if contains_unit(value_str):
        # unit `jt` is only for lang=id (Indonesia)
        if CurrencyUnit.ID_JT.value in value_str or CurrencyUnit.ID_RB.value in value_str:
            value_unit = value_str[-2]
            value = clean_currency(value_str[:-2], lang)
        else:
            value_unit = value_str[-1]
            value = clean_currency(value_str[:-1], lang)
    else:
        value_unit = ""
        value = clean_currency(value_str, lang)

    empty_percent = False
    if percent_str == "—":
        empty_percent = True

    percent: float = get_percent_value(percent_str, lang)

    # builds percent change value
    percent_change: str = ValueChange.NONE.value
    if percent == "—":
        percent_change = ValueChange.NONE.value
    elif percent > 0:
        percent_change = ValueChange.INCREASE.value
    elif percent < 0:
        percent_change = ValueChange.DECREASE.value

    # builds price change value
    price_change: str = ValueChange.NONE.value
    if value == "—":
        price_change = ValueChange.INCREASE.value
    elif value > 0:
        price_change = ValueChange.INCREASE.value
    elif value < 0:
        price_change = ValueChange.DECREASE.value

    return FinancialValue(
        unit=value_unit,
        value=value,
        percent=percent,
        price_change=price_change,
        percent_change=percent_change,
        empty_percent=empty_percent,
    )
