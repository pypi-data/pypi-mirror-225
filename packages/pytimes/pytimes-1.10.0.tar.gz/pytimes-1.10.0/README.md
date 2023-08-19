A small helper package for working with time intervals.

This package provides a single class called `Seconds` (a subclass of `int`) that
represents a time interval in seconds. It also provides a number of constants that
represent common time intervals, such as `ONE_SECOND` and `ONE_DAY`.

The intended use of this package is to provide a more readable alternative to using
raw numbers for time intervals. For example, instead of writing `time.sleep(86400)`
to sleep for one day, you can write `time.sleep(ONE_DAY)`. This makes the code more
readable and easier to understand.

The `Seconds` class also provides attributes for accessing the interval in other
units of time, such as `minutes` and `hours`.

Shoot me an email if you use it and find it useful, or if you have any suggestions!

# Usage
```python
>>> from times import THREE_MINUTES
>>> import time
>>> time.sleep(THREE_MINUTES)
```
```python
>>> import times
>>> times.ONE_DAY
86400
>>> times.THREE_HOURS.years
0.00034223866072692215
>>> times.FIVE_MONTHS.minutes
219145.25
```
```python
from times import Seconds, TEN_YEARS
>>> century = Seconds(TEN_YEARS * 10)
>>> century
3155692500
>>> century.hours
876581.25
```

# Installation
```bash
pip install pytimes
```

# Reference
The `Seconds` class is a subclass of `int` that represents a time interval in seconds. It usually won't be instantiated directly, but rather used via the constants defined in this module. It offers the following
attributes:

* `seconds`: The interval in seconds.
* `minutes`: The interval in minutes.
* `hours`: The interval in hours.
* `days`: The interval in days.
* `weeks`: The interval in weeks.
* `months`: The interval in months. A month is defined as 1/12 of a year.
* `years`: The interval in years. A year is defined as 365.242196 days.

The following constants are defined in this module:
* `ONE_SECOND`
* `ONE_MINUTE`
* `ONE_HOUR`
* `ONE_DAY`
* `ONE_WEEK`
* `ONE_MONTH`
* `ONE_YEAR`
* ... And many more, in variations like `TWO_DAYS`, `THREE_WEEKS`, `FOUR_MONTHS`, etc.


# Requirements
Python 3.6+



# License
MIT


