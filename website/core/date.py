from datetime import datetime

from django.conf import settings
from django.utils import timezone

day_endings = {
    0: 'th',
    1: 'st',
    2: 'nd',
    3: 'rd',
    21: 'st',
    22: 'nd',
    23: 'rd',
    31: 'st'
}


def format_day_with_ending(day: int) -> str:
    if day in day_endings:
        suffix = day_endings[day]
    else:
        suffix = day_endings[0]
    return "%d%s" % (day, suffix)


def format_month_day_year_long(date: datetime) -> str:
    """ July 9th, 2022 """
    return "%s %s, %d" % (
        date.strftime('%B'),
        format_day_with_ending(date.day),
        date.year
    )


def format_month_day_long(date: datetime) -> str:
    """ July 9th """
    return "%s %s" % (
        date.strftime('%B'),
        format_day_with_ending(date.day)
    )


def is_passed_rsvp_deadline() -> bool:
    return settings.DATE_RSVP_DEADLINE < timezone.now()
