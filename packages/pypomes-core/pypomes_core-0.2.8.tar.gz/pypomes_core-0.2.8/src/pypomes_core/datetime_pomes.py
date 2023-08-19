import pytz
from datetime import date, datetime
from dateutil import parser
from typing import Final

from .env_pomes import APP_PREFIX, env_get_str

# some useful date/datetime formats
DATE_FORMAT_STD: Final[str] = "%m/%d/%Y"
DATE_FORMAT_COMPACT: Final[str] = "%Y%m%d"
DATE_FORMAT_INV: Final[str] = "%Y-%m-%d"
DATETIME_FORMAT_STD: Final[str] = "%m/%d/%Y %H:%M:%S"
DATETIME_FORMAT_COMPACT: Final[str] = "%Y%m%d%H%M%S"
DATETIME_FORMAT_INV: Final[str] = "%Y-%m-%d %H:%M:%S"

TIMEZONE_LOCAL: pytz.BaseTzInfo = pytz.timezone(env_get_str(f"{APP_PREFIX}_TIMEZONE_LOCAL", "America/Sao_Paulo"))
TIMEZONE_UTC: pytz.BaseTzInfo = pytz.UTC


def date_reformat(dt_str: str, to_format: str, **kwargs: any) -> str:
    """
    Convert the date in *dt_str* to the format especified in *to_format*.

    The argument *dt_str* must represent a valid date, with or without time-of-day information.
    The argument *to_format* must be a valid format for *date* ou *datetime*.

    :param dt_str: The date to convert.
    :param to_format: The format for the conversion.
    :param kwargs: Optional arguments for the parser in python-dateutil ('dayfirst' is a common argument).
    :return:  The converted date.
    """
    result: str | None = None
    ts: datetime = parser.parse(dt_str, **kwargs)
    if ts is not None:
        result = datetime.strftime(ts, to_format)

    return result


def date_parse(dt_str: str, **kwargs: any) -> date:
    """
    Obtain and return the *date* object corresponding to *dt_str*.

    Return *None* se *dt_str* does not contain a valid date.

    :param dt_str: The date, in a supported format.
    :param kwargs: Optional arguments for the parser in python-dateutil ('dayfirst' is a common argument).
    :return: The corresponding date object, or None.
    """
    result: date | None = None
    if dt_str is not None:
        result = parser.parse(dt_str, **kwargs).date()

    return result


def datetime_parse(dt_str: str, **kwargs: any) -> datetime:
    """
    Obtain and return the *datetime* object corresponding to *dt_str*.

   Return *None* se *dt_str* does not contain a valid date.

    :param dt_str: The date, in a supported format.
    :param kwargs: Optional arguments for the parser in python-dateutil ('dayfirst' is a common argument).
    :return: The corresponding datetime object, or None.
    """
    result: datetime | None = None
    if dt_str is not None:
        result = parser.parse(dt_str, **kwargs)

    return result
