from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Dict

import holidays
import pytz
import requests
from dateutil.relativedelta import relativedelta

from premium_bond_checker.exceptions import InvalidHolderNumberException


class BondPeriod:
    THIS_MONTH = "this_month"
    LAST_SIX_MONTHS = "last_six_month"
    UNCLAIMED = "unclaimed_prize"

    @classmethod
    def all(cls) -> list:
        return [cls.THIS_MONTH, cls.LAST_SIX_MONTHS, cls.UNCLAIMED]


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
        today = date.today()

        this_month_draw = self._get_draw_date(today, 0)
        if today.day <= this_month_draw.day:
            return this_month_draw

        return self._get_draw_date(today, 1)

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

    def _get_draw_date(self, today: date, month_offset: int) -> date:
        offset_month = today + relativedelta(months=month_offset)
        first_day_of_month = offset_month.replace(day=1)
        uk_holidays = holidays.UnitedKingdom(years=first_day_of_month.year)
        while first_day_of_month.weekday() >= 5 or first_day_of_month in uk_holidays:
            first_day_of_month += timedelta(days=1)

        return first_day_of_month
