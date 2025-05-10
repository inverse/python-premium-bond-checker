from datetime import date, datetime, timedelta

import holidays
import pytz
from dateutil.relativedelta import relativedelta


def current_date_london() -> date:
    return datetime.now(pytz.timezone("Europe/London")).date()


def get_draw_date(today: date, month_offset: int) -> date:
    offset_month = today + relativedelta(months=month_offset)
    first_day_of_month = offset_month.replace(day=1)
    uk_holidays = holidays.UnitedKingdom(years=first_day_of_month.year)
    while first_day_of_month.weekday() >= 5 or first_day_of_month in uk_holidays:
        first_day_of_month += timedelta(days=1)

    return first_day_of_month
