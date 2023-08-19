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

SIX_SECONDS = Seconds(ONE_SECOND * 6)
SIX_MINUTES = Seconds(ONE_MINUTE * 6)
SIX_HOURS = Seconds(ONE_HOUR * 6)
SIX_DAYS = Seconds(ONE_DAY * 6)
SIX_WEEKS = Seconds(ONE_WEEK * 6)
SIX_MONTHS = Seconds(ONE_MONTH * 6)
SIX_YEARS = Seconds(ONE_YEAR * 6)

SEVEN_SECONDS = Seconds(ONE_SECOND * 7)
SEVEN_MINUTES = Seconds(ONE_MINUTE * 7)
SEVEN_HOURS = Seconds(ONE_HOUR * 7)
SEVEN_DAYS = Seconds(ONE_DAY * 7)
SEVEN_WEEKS = Seconds(ONE_WEEK * 7)
SEVEN_MONTHS = Seconds(ONE_MONTH * 7)
SEVEN_YEARS = Seconds(ONE_YEAR * 7)

EIGHT_SECONDS = Seconds(ONE_SECOND * 8)
EIGHT_MINUTES = Seconds(ONE_MINUTE * 8)
EIGHT_HOURS = Seconds(ONE_HOUR * 8)
EIGHT_DAYS = Seconds(ONE_DAY * 8)
EIGHT_WEEKS = Seconds(ONE_WEEK * 8)
EIGHT_MONTHS = Seconds(ONE_MONTH * 8)
EIGHT_YEARS = Seconds(ONE_YEAR * 8)

NINE_SECONDS = Seconds(ONE_SECOND * 9)
NINE_MINUTES = Seconds(ONE_MINUTE * 9)
NINE_HOURS = Seconds(ONE_HOUR * 9)
NINE_DAYS = Seconds(ONE_DAY * 9)
NINE_WEEKS = Seconds(ONE_WEEK * 9)
NINE_MONTHS = Seconds(ONE_MONTH * 9)
NINE_YEARS = Seconds(ONE_YEAR * 9)

TEN_SECONDS = Seconds(ONE_SECOND * 10)
TEN_MINUTES = Seconds(ONE_MINUTE * 10)
TEN_HOURS = Seconds(ONE_HOUR * 10)
TEN_DAYS = Seconds(ONE_DAY * 10)
TEN_WEEKS = Seconds(ONE_WEEK * 10)
TEN_MONTHS = Seconds(ONE_MONTH * 10)
TEN_YEARS = Seconds(ONE_YEAR * 10)

FIFTEEN_SECONDS = Seconds(ONE_SECOND * 15)
FIFTEEN_MINUTES = Seconds(ONE_MINUTE * 15)
FIFTEEN_HOURS = Seconds(ONE_HOUR * 15)
FIFTEEN_DAYS = Seconds(ONE_DAY * 15)
FIFTEEN_WEEKS = Seconds(ONE_WEEK * 15)
FIFTEEN_MONTHS = Seconds(ONE_MONTH * 15)
FIFTEEN_YEARS = Seconds(ONE_YEAR * 15)

THIRTY_SECONDS = Seconds(ONE_SECOND * 30)
THIRTY_MINUTES = Seconds(ONE_MINUTE * 30)
THIRTY_HOURS = Seconds(ONE_HOUR * 30)
THIRTY_DAYS = Seconds(ONE_DAY * 30)
THIRTY_WEEKS = Seconds(ONE_WEEK * 30)
THIRTY_MONTHS = Seconds(ONE_MONTH * 30)
THIRTY_YEARS = Seconds(ONE_YEAR * 30)

FOURTYFIVE_SECONDS = Seconds(ONE_SECOND * 45)
FOURTYFIVE_MINUTES = Seconds(ONE_MINUTE * 45)
FOURTYFIVE_HOURS = Seconds(ONE_HOUR * 45)
FOURTYFIVE_DAYS = Seconds(ONE_DAY * 45)
FOURTYFIVE_WEEKS = Seconds(ONE_WEEK * 45)
FOURTYFIVE_MONTHS = Seconds(ONE_MONTH * 45)
FOURTYFIVE_YEARS = Seconds(ONE_YEAR * 45)

SIXTY_SECONDS = Seconds(ONE_SECOND * 60)
SIXTY_MINUTES = Seconds(ONE_MINUTE * 60)
SIXTY_HOURS = Seconds(ONE_HOUR * 60)
SIXTY_DAYS = Seconds(ONE_DAY * 60)
SIXTY_WEEKS = Seconds(ONE_WEEK * 60)
SIXTY_MONTHS = Seconds(ONE_MONTH * 60)
SIXTY_YEARS = Seconds(ONE_YEAR * 60)

NINETY_SECONDS = Seconds(ONE_SECOND * 90)
NINETY_MINUTES = Seconds(ONE_MINUTE * 90)
NINETY_HOURS = Seconds(ONE_HOUR * 90)
NINETY_DAYS = Seconds(ONE_DAY * 90)
NINETY_WEEKS = Seconds(ONE_WEEK * 90)
NINETY_MONTHS = Seconds(ONE_MONTH * 90)
NINETY_YEARS = Seconds(ONE_YEAR * 90)
