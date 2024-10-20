
# KlineTimestamp

KlineTimestamp is a Python library designed to efficiently handle timestamps within discrete time intervals, commonly known as klines or candlesticks, often used in financial data analysis. This library simplifies the management of Unix timestamps (in milliseconds) for applications that work with time series data, particularly those involving financial market data.

Project: https://github.com/nand0san/KlineTimestamp/tree/github

## Features

- **Calculate Opening and Closing Timestamps**: Easily obtain the opening and closing timestamps of a kline based on specified intervals.
- **Timezone Support**: Handle different timezones with correct Daylight Saving Time (DST) adjustments.
- **Convert to Common Date-Time Objects**: Convert timestamps to `datetime.datetime` and `pandas.Timestamp` objects for seamless integration with other libraries.
- **Arithmetic Operations**: Modify timestamps using `timedelta` objects, and perform arithmetic operations between klines.
- **Navigation Between Klines**: Retrieve the next or previous kline's opening and closing timestamps.
- **Comparison Methods**: Compare klines using standard comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`).
- **Robust Equality Checks**: Determine if two klines represent the same time interval, considering interval and timezone.

## Installation

Install the library using `pip`:

```bash
pip install kline_timestamp
```

## Dependencies

- Python 3.x
- [`pytz`](https://pypi.org/project/pytz/)
- [`pandas`](https://pypi.org/project/pandas/)

## Usage

### Importing the Library

```python
from kline_timestamp import KlineTimestamp
from datetime import timedelta
```

### Creating a KlineTimestamp Instance

```python
# Create an instance with a specific timestamp, interval, and timezone
kt = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='Europe/Madrid')
```

### Getting Opening and Closing Timestamps

```python
# Get the opening timestamp in milliseconds
open_ts_ms = kt.get_candle_open_timestamp_ms()
print(f"Open timestamp (ms): {open_ts_ms}")

# Get the closing timestamp in milliseconds
close_ts_ms = kt.get_candle_close_timestamp_ms()
print(f"Close timestamp (ms): {close_ts_ms}")

# Access opening and closing timestamps as attributes
print(f"Open as attribute: {kt.open}")
print(f"Close as attribute: {kt.close}")
```

### Converting to Datetime Objects

```python
# Convert to datetime in the specified timezone
dt = kt.to_datetime()
print(f"Datetime: {dt}")

# Convert to pandas Timestamp
pd_ts = kt.to_pandas_timestamp()
print(f"Pandas Timestamp: {pd_ts}")
```

### String Representation

```python
# String representation of the KlineTimestamp instance
print(f"String representation: {str(kt)}")
print(f"Representation: {repr(kt)}")
```

### Updating Timezone

```python
# Update the timezone of the instance
kt.update_timezone('UTC')
print(f"Updated timezone: {kt.tzinfo}")
print(kt)
```

### Arithmetic Operations with Timedelta

```python
# Add a timedelta to the timestamp
kt_added = kt + timedelta(hours=1)
print(f"Timestamp after adding 1 hour: {kt_added.to_datetime()}")

# Subtract a timedelta from the timestamp
kt_subtracted = kt - timedelta(hours=1)
print(f"Timestamp after subtracting 1 hour: {kt_subtracted.to_datetime()}")
```

### Subtracting Two KlineTimestamp Instances

```python
# Create another KlineTimestamp instance
kt_other = KlineTimestamp(timestamp_ms=1633033200000, interval='1h', tzinfo='UTC')

# Subtract two KlineTimestamp instances to get a timedelta
time_diff = kt - kt_other
print(f"Time difference between kt and kt_other: {time_diff}")
```

### Navigating Between Klines

```python
# Get the next kline
kt_next = kt.next()
print(f"Next candle timestamp: {kt_next.to_datetime()}")

# Get the previous kline
kt_prev = kt.prev()
print(f"Previous candle timestamp: {kt_prev.to_datetime()}")
```

### Comparison Methods

```python
# Compare two KlineTimestamp instances
print(f"kt == kt_other: {kt == kt_other}")
print(f"kt > kt_other: {kt > kt_other}")
print(f"kt < kt_other: {kt < kt_other}")
print(f"kt >= kt_other: {kt >= kt_other}")
print(f"kt <= kt_other: {kt <= kt_other}")

# Equality with the same parameters
kt_same = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='UTC')
print(f"kt == kt_same: {kt == kt_same}")
```

## Supported Intervals

The following intervals are supported:

- `'1m'`: 1 minute
- `'3m'`: 3 minutes
- `'5m'`: 5 minutes
- `'15m'`: 15 minutes
- `'30m'`: 30 minutes
- `'1h'`: 1 hour
- `'2h'`: 2 hours
- `'4h'`: 4 hours
- `'6h'`: 6 hours
- `'8h'`: 8 hours
- `'12h'`: 12 hours
- `'1d'`: 1 day
- `'3d'`: 3 days
- `'1w'`: 1 week

## API Reference

### Class: `KlineTimestamp`

#### Initialization

```python
KlineTimestamp(timestamp_ms: int, interval: str, tzinfo='UTC')
```

- **Parameters**:
  - `timestamp_ms` (int): The timestamp in milliseconds.
  - `interval` (str): The interval of the kline. Must be one of the supported intervals.
  - `tzinfo` (str or pytz.timezone, optional): The timezone of the timestamp. Defaults to `'UTC'`.

- **Raises**:
  - `ValueError`: If the interval is not valid.
  - `TypeError`: If `tzinfo` is neither a string nor a `pytz.timezone` object.

#### Attributes

- `timestamp_ms` (int): The original timestamp in milliseconds.
- `interval` (str): The interval of the kline.
- `tzinfo` (`pytz.timezone`): The timezone of the timestamp.
- `open` (int): The opening timestamp of the kline in milliseconds.
- `close` (int): The closing timestamp of the kline in milliseconds.

#### Methods

- `get_candle_open_timestamp_ms() -> int`: Returns the opening timestamp of the current kline in milliseconds.
- `get_candle_close_timestamp_ms() -> int`: Returns the closing timestamp of the current kline in milliseconds.
- `to_datetime() -> datetime`: Converts the opening timestamp to a `datetime` object in the specified timezone.
- `to_pandas_timestamp() -> pd.Timestamp`: Converts the opening timestamp to a `pandas.Timestamp` object in the specified timezone.
- `update_timezone(tzinfo: Union[str, pytz.BaseTzInfo]) -> None`: Updates the timezone of the KlineTimestamp instance.
- `__add__(other: timedelta) -> KlineTimestamp`: Adds a `timedelta` to the timestamp, returning a new `KlineTimestamp` instance.
- `__sub__(other: Union[timedelta, KlineTimestamp]) -> Union[KlineTimestamp, timedelta]`: Subtracts a `timedelta` or another `KlineTimestamp` from this instance.
- `next() -> KlineTimestamp`: Returns a new `KlineTimestamp` representing the next kline.
- `prev() -> KlineTimestamp`: Returns a new `KlineTimestamp` representing the previous kline.
- Comparison methods: `__eq__`, `__lt__`, `__le__`, `__gt__`, `__ge__` for comparing klines.

## Example

Here's a complete example demonstrating how to use the `KlineTimestamp` class:

```python
from kline_timestamp import KlineTimestamp
from datetime import timedelta

# Initialize a KlineTimestamp instance
kt = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='Europe/Madrid')

# Print opening and closing timestamps
print(f"Open timestamp (ms): {kt.open}")
print(f"Close timestamp (ms): {kt.close}")

# Convert to datetime and pandas Timestamp
print(f"Datetime: {kt.to_datetime()}")
print(f"Pandas Timestamp: {kt.to_pandas_timestamp()}")

# Update timezone
kt.update_timezone('UTC')
print(f"Updated timezone: {kt.tzinfo}")
print(f"Datetime in UTC: {kt.to_datetime()}")

# Arithmetic operations with timedelta
kt_plus_one_hour = kt + timedelta(hours=1)
print(f"Timestamp after adding 1 hour: {kt_plus_one_hour.to_datetime()}")

kt_minus_one_hour = kt - timedelta(hours=1)
print(f"Timestamp after subtracting 1 hour: {kt_minus_one_hour.to_datetime()}")

# Navigate to next and previous klines
next_kt = kt.next()
prev_kt = kt.prev()
print(f"Next kline datetime: {next_kt.to_datetime()}")
print(f"Previous kline datetime: {prev_kt.to_datetime()}")

# Compare klines
kt_other = KlineTimestamp(timestamp_ms=1633033200000, interval='1h', tzinfo='UTC')
print(f"kt == kt_other: {kt == kt_other}")
print(f"kt > kt_other: {kt > kt_other}")

# Time difference between two klines
time_difference = kt - kt_other
print(f"Time difference: {time_difference}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Author

[nand0san](https://github.com/nand0san)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/nand0san/KlineTimestamp/tree/github).

## Contact

For any questions or suggestions, please contact using github.

## Acknowledgments

- Inspired by the need for efficient timestamp management in financial data analysis.
- Thanks to the contributors of `pytz` and `pandas` for providing essential tools for timezone and data handling.
