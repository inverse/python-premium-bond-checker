from datetime import date
from typing import List

import requests

from .exceptions import InvalidHolderNumberException
from .models import CheckResult, Result
from .utils import current_date_london, get_draw_date


class BondPeriod:
    THIS_MONTH = "this_month"
    LAST_SIX_MONTHS = "last_six_month"
    UNCLAIMED = "unclaimed_prize"

    @classmethod
    def all(cls) -> List[str]:
        return [cls.THIS_MONTH, cls.LAST_SIX_MONTHS, cls.UNCLAIMED]


class Client:
    BASE_URL = "https://www.nsandi.com"

    @staticmethod
    def next_draw() -> date:
        today_london = current_date_london()

        this_month_draw = get_draw_date(today_london, 0)
        if today_london.day <= this_month_draw.day:
            return this_month_draw

        return get_draw_date(today_london, 1)

    def check(self, holder_number: str) -> CheckResult:
        check_result = CheckResult()
        check_result.add_result(self.check_this_month(holder_number))
        check_result.add_result(self.check_last_six_months(holder_number))
        check_result.add_result(self.check_unclaimed(holder_number))
        return check_result

    def check_this_month(self, holder_number: str) -> Result:
        return self._do_request(holder_number, BondPeriod.THIS_MONTH)

    def check_last_six_months(self, holder_number: str) -> Result:
        return self._do_request(holder_number, BondPeriod.LAST_SIX_MONTHS)

    def check_unclaimed(self, holder_number: str) -> Result:
        return self._do_request(holder_number, BondPeriod.UNCLAIMED)

    def is_holder_number_valid(self, holder_number: str) -> bool:
        try:
            self.check_this_month(holder_number)
        except InvalidHolderNumberException:
            return False

        return True

    def _do_request(self, holder_number: str, bond_period: str) -> Result:
        url = f"{self.BASE_URL}/premium-bonds-have-i-won-ajax"
        response = requests.post(
            url,
            data={
                "field_premium_bond_period": bond_period,
                "field_premium_bond_number": holder_number,
            },
        )

        response.raise_for_status()
        json = response.json()

        if json["holder_number"] == "is invalid":
            raise InvalidHolderNumberException(f"{holder_number} is an invalid number")

        won = json["status"] == "win"
        header = json["header"]
        tagline = json["tagline"]
        return Result(won, holder_number, bond_period, header, tagline)
