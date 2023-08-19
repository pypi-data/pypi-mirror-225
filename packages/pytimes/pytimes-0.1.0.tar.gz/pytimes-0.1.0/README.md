A small helper package for working with time intervals.

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

# Usage
```python
>>> import pytimes
>>> pytimes.ONE_DAY
86400
>>> pytimes.ONE_DAY.hours
24
```

# Requirements
Python 3.6+


# Installation
```bash
pip install pytimes
```

# License
MIT


