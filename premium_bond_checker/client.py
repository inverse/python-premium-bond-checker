from dataclasses import dataclass
from typing import Dict

import requests

from .exceptions import InvalidHolderNumberException


class ResultType:
    THIS_MONTH = "this_month"
    LAST_SIX_MONTHS = "last_six_months"
    UNCLAIMED = "unclaimed"


@dataclass
class Result:
    won: bool
    holder_number: str
    bond_period: str


class CheckResult:
    def __init__(self):
        self.results: Dict[str, Result] = {}

    def add_result(self, key: str, result: Result):
        self.results[key] = result

    def has_won(self) -> bool:
        return any([result.won for result in list(self.results.values())])


class Client:
    BASE_URL = "https://www.nsandi.com/"

    def check(self, holder_number: str) -> CheckResult:
        check_result = CheckResult()
        check_result.add_result(
            ResultType.THIS_MONTH, self.check_this_month(holder_number)
        )
        check_result.add_result(
            ResultType.LAST_SIX_MONTHS, self.check_last_six_months(holder_number)
        )
        check_result.add_result(
            ResultType.UNCLAIMED, self.check_unclaimed(holder_number)
        )
        return check_result

    def check_this_month(self, holder_number: str) -> Result:
        return self._do_request(holder_number, "this_month")

    def check_last_six_months(self, holder_number: str) -> Result:
        return self._do_request(holder_number, "last_six_month")

    def check_unclaimed(self, holder_number: str) -> Result:
        return self._do_request(holder_number, "unclaimed_prize")

    def is_holder_number_valid(self, holder_number: str) -> bool:
        try:
            self.check_this_month(holder_number)
        except InvalidHolderNumberException:
            return False

        return True

    def _do_request(self, holder_number: str, bond_period: str) -> Result:
        url = f"{self.BASE_URL}premium-bonds-have-i-won-ajax"
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
        return Result(won, holder_number, bond_period)
