from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict

import pytz
import requests
from bs4 import BeautifulSoup

from premium_bond_checker.exceptions import (
    InvalidHolderNumberException,
    PremiumBondCheckerException,
)


class BondPeriod:
    THIS_MONTH = "this_month"
    LAST_SIX_MONTHS = "last_six_month"
    UNCLAIMED = "unclaimed_prize"


@dataclass
class Result:
    won: bool
    holder_number: str
    bond_period: str
    header: str
    tagline: str


class CheckResult:
    def __init__(self):
        self.results: Dict[str, Result] = {}

    def add_result(self, result: Result):
        self.results[result.bond_period] = result

    def has_won(self) -> bool:
        return any([result.won for result in list(self.results.values())])


class Client:
    BASE_URL = "https://www.nsandi.com"

    def next_draw(self) -> date:
        try:
            response = requests.get(f"{self.BASE_URL}/prize-checker", timeout=10)
            response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
            html_content = response.text
        except requests.RequestException as e:
            raise PremiumBondCheckerException(f"Failed to get prize checker page: {e}")

        soup = BeautifulSoup(html_content, "html.parser")
        days_remaining_element = soup.find_all(class_="pb-countdown-timer-value")

        if not days_remaining_element or len(days_remaining_element) == 0:
            raise PremiumBondCheckerException(
                "Prize draw page did not contain any days remaining element"
            )

        days_remaining = int(days_remaining_element[0].text.strip())
        current_date = self._current_date_gmt()

        return current_date + timedelta(days=days_remaining)

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

    def _current_date_gmt(self) -> date:
        gmt_timezone = pytz.timezone("GMT")
        return datetime.now(gmt_timezone).date()
