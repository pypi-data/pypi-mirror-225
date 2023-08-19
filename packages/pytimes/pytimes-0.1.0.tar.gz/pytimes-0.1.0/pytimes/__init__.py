"""A small helper package for working with time intervals.

This package provides a single class, `Seconds`, which is a subclass of `int` that
represents a time interval in seconds. It also provides a number of constants that
represent common time intervals, such as `ONE_SECOND` and `ONE_DAY`.

The intended use of this package is to provide a more readable alternative to using
raw numbers for time intervals. For example, instead of writing `time.sleep(86400)`
to sleep for one day, you can write `time.sleep(ONE_DAY)`. This makes the code more
readable and easier to understand.

The `Seconds` class also provides attributes for accessing the interval in other
units of time, such as `minutes` and `hours`. For example, `ONE_DAY.minutes` is
equivalent to `ONE_DAY / 60`, and `ONE_DAY.hours` is equivalent to `ONE_DAY / 60 / 60`.
"""

_YEAR_DAYS = 365.242196
"Days per year, as per the National Institute of Standards and Technology"

_MONTH_DAYS = _YEAR_DAYS / 12
"Average days per month, as per the National Institute of Standards and Technology."


class Seconds(int):
    """A time interval, expressed in seconds.

    Other units of time can be accessed as attributes, such as `minutes` and `hours`.
    """

    def __new__(cls, seconds: float) -> "Seconds":
        return super().__new__(cls, seconds)

    @property
    def seconds(self) -> int:
        return self

    @property
    def minutes(self) -> float:
        return self / 60

    @property
    def hours(self) -> float:
        return self / 60 / 60

    @property
    def days(self) -> float:
        return self / 60 / 60 / 24

    @property
    def weeks(self) -> float:
        return self / 60 / 60 / 24 / 7

    @property
    def months(self) -> float:
        """The interval in average months.

        A month is defined as 1/12 of a year, which is 365.242196 days.
        """

        return self / 60 / 60 / 24 / _MONTH_DAYS

    @property
    def years(self) -> float:
        """The interval in years.

        A year is defined as 365.242196 days.
        """
        return self / 60 / 60 / 24 / _YEAR_DAYS


ONE_SECOND = Seconds(1)
ONE_MINUTE = Seconds(60)
ONE_HOUR = Seconds(60 * 60)
ONE_DAY = Seconds(60 * 60 * 24)
ONE_WEEK = Seconds(ONE_DAY * 7)
ONE_MONTH = Seconds(ONE_DAY * _MONTH_DAYS)
ONE_YEAR = Seconds(ONE_DAY * _YEAR_DAYS)

TWO_SECONDS = Seconds(ONE_SECOND * 2)
TWO_MINUTES = Seconds(ONE_MINUTE * 2)
TWO_HOURS = Seconds(ONE_HOUR * 2)
TWO_DAYS = Seconds(ONE_DAY * 2)
TWO_WEEKS = Seconds(ONE_WEEK * 2)
TWO_MONTHS = Seconds(ONE_MONTH * 2)
TWO_YEARS = Seconds(ONE_YEAR * 2)

THREE_SECONDS = Seconds(ONE_SECOND * 3)
THREE_MINUTES = Seconds(ONE_MINUTE * 3)
THREE_HOURS = Seconds(ONE_HOUR * 3)
THREE_DAYS = Seconds(ONE_DAY * 3)
THREE_WEEKS = Seconds(ONE_WEEK * 3)
THREE_MONTHS = Seconds(ONE_MONTH * 3)
THREE_YEARS = Seconds(ONE_YEAR * 3)

FOUR_SECONDS = Seconds(ONE_SECOND * 4)
FOUR_MINUTES = Seconds(ONE_MINUTE * 4)
FOUR_HOURS = Seconds(ONE_HOUR * 4)
FOUR_DAYS = Seconds(ONE_DAY * 4)
FOUR_WEEKS = Seconds(ONE_WEEK * 4)
FOUR_MONTHS = Seconds(ONE_MONTH * 4)
FOUR_YEARS = Seconds(ONE_YEAR * 4)

FIVE_SECONDS = Seconds(ONE_SECOND * 5)
FIVE_MINUTES = Seconds(ONE_MINUTE * 5)
FIVE_HOURS = Seconds(ONE_HOUR * 5)
FIVE_DAYS = Seconds(ONE_DAY * 5)
FIVE_WEEKS = Seconds(ONE_WEEK * 5)
FIVE_MONTHS = Seconds(ONE_MONTH * 5)
FIVE_YEARS = Seconds(ONE_YEAR * 5)
