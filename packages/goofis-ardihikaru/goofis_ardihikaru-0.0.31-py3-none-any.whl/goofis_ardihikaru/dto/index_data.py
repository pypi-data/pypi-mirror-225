from dataclasses import dataclass, asdict
from typing import Dict, Union, Any

import simplejson as json


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


@dataclass
class IndexData:
    """ Index data model """

    FN_ID = "id"
    FN_GENERAL = "general"
    FN_ABOUT = "about"
    FN_CURRENT_PRICE_CHANGE_PERCENT = "current_price_change_percent"
    FN_CURRENT_PRICE_CHANGE_VALUE = "current_price_change_value"

    id: str = "-1"
    general: General = General()
    name: str = ""
    about: str = ""
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
