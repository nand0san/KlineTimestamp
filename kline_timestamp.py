from typing import Union
from datetime import datetime, timedelta
import pytz
import pandas as pd


class KlineTimestamp:

    def __init__(self, timestamp_ms: int, interval: str, tzinfo='UTC'):
        """
        Initializes a new instance of the KlineTimestamp class.

        The `timestamp_ms` parameter represents the timestamp in milliseconds. It is a required input.

        The `interval` parameter specifies the interval of the timestamp. If an invalid interval is provided, a ValueError will be raised.

        Default kline sizes are: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w.

        The `tzinfo` parameter represents the timezone of the timestamp. It is an optional parameter that defaults to 'UTC'. If a string is provided as the timezone, it should be a valid IANA timezone identifier. If a pytz.timezone object is provided, it should be the timezone of the timestamp.

        If the `interval` parameter is not valid, a ValueError will be raised.

        The `__init__` method initializes the `interval`, `tick_ms`, `timestamp_ms`, and `tzinfo` attributes of the KlineTimestamp instance. It also raises a ValueError if the `interval` parameter is not valid.

        :param timestamp_ms: The timestamp in milliseconds.
        :type timestamp_ms: int
        :param interval: The interval of the timestamp.
        :type interval: str
        :param tzinfo: The timezone of the timestamp. Default is 'UTC'.
        :type tzinfo: str or pytz.timezone, optional. Default is 'UTC'.

        :raises ValueError: If the interval is not valid.
        """

        tick_milliseconds = {
            '1m': 60 * 1000,
            '3m': 3 * 60 * 1000,
            '5m': 5 * 60 * 1000,
            '15m': 15 * 60 * 1000,
            '30m': 30 * 60 * 1000,
            '1h': 60 * 60 * 1000,
            '2h': 2 * 60 * 60 * 1000,
            '4h': 4 * 60 * 60 * 1000,
            '6h': 6 * 60 * 60 * 1000,
            '8h': 8 * 60 * 60 * 1000,
            '12h': 12 * 60 * 60 * 1000,
            '1d': 24 * 60 * 60 * 1000,
            '3d': 3 * 24 * 60 * 60 * 1000,
            '1w': 7 * 24 * 60 * 60 * 1000
        }

        if interval not in tick_milliseconds:
            raise ValueError(f"Invalid interval: {interval}. Valid intervals are: {list(tick_milliseconds.keys())}.")
        self.interval = interval
        self.tick_ms = tick_milliseconds[interval]
        self.timestamp_ms = int(timestamp_ms)

        if isinstance(tzinfo, str):
            self.tzinfo = pytz.timezone(tzinfo)
        else:
            self.tzinfo = tzinfo

    def get_candle_open_timestamp_ms(self) -> int:
        """
        This method returns the timestamp of the opening of the current candle (K-line) in milliseconds.

        The timestamp is calculated by dividing the provided timestamp by the tick size (milliseconds per interval) and then multiplying it back by the tick size.

        :return: The timestamp of the opening of the current candle in milliseconds.
        """
        return (self.timestamp_ms // self.tick_ms) * self.tick_ms

    def get_candle_close_timestamp_ms(self) -> int:
        """
        This method returns the timestamp of the closing of the current candle (K-line) in milliseconds.

        The timestamp is calculated by adding the tick size (milliseconds per interval) minus one millisecond to the opening timestamp.

        :return: The timestamp of the closing of the current candle in milliseconds.
        """
        return self.get_candle_open_timestamp_ms() + self.tick_ms - 1

    def to_datetime(self) -> datetime:
        """
        This method returns the datetime object of the current open time for candle (K-line) in the provided timezone.

        :return: The datetime object of the current open time for candle (K-line) in the provided time zone.
        """
        dt_utc = datetime.utcfromtimestamp(self.get_candle_open_timestamp_ms() / 1000)
        dt_utc = dt_utc.replace(tzinfo=pytz.utc)
        dt_local = dt_utc.astimezone(self.tzinfo)
        return dt_local

    def to_pandas_timestamp(self) -> pd.Timestamp:
        """
        This method returns the pandas Timestamp object of the current open time for candle (K-line) in the provided timezone.

        :return: The pandas Timestamp object of the current open time for candle (K-line) in the provided time zone.
        """
        return pd.Timestamp(self.get_candle_open_timestamp_ms(), unit='ms', tz='UTC').tz_convert(self.tzinfo)

    def __str__(self):
        """
        This method returns a string representation of the KlineTimestamp instance. The string includes the ISO format of the datetime object, the interval, and the timezone.

        :return: A string representation of the KlineTimestamp instance.
        """
        return f"KlineTimestamp({self.to_datetime().isoformat()}, interval='{self.interval}', tz='{self.tzinfo.zone}')"

    __repr__ = __str__

    def update_timezone(self, tzinfo: Union[str, pytz.BaseTzInfo]) -> None:
        """
        Updates the timezone of the KlineTimestamp instance.

        :param tzinfo: The new timezone, either as a string or pytz.timezone object.
        :raises TypeError: If `tzinfo` is neither a string nor a pytz.timezone object.
        """
        if isinstance(tzinfo, str):
            self.tzinfo = pytz.timezone(tzinfo)
        elif isinstance(tzinfo, pytz.BaseTzInfo):
            self.tzinfo = tzinfo
        else:
            raise TypeError("tzinfo must be a string or pytz.timezone object")

    def __add__(self, other: timedelta) -> 'KlineTimestamp':
        """
        Adds a timedelta to this instance.

        :param other: The timedelta to add.
        :return: A new KlineTimestamp.
        :raises TypeError: If `other` is not a timedelta.
        """
        if isinstance(other, timedelta):
            new_timestamp_ms = self.timestamp_ms + int(other.total_seconds() * 1000)
            return KlineTimestamp(new_timestamp_ms, interval=self.interval, tzinfo=self.tzinfo)
        else:
            raise TypeError(f"Unsupported type for +: 'KlineTimestamp' and '{type(other).__name__}'")

    def __sub__(self, other: Union[timedelta, 'KlineTimestamp']) -> Union['KlineTimestamp', timedelta]:
        """
        Subtracts a timedelta or another KlineTimestamp from this instance.

        :param other: The timedelta or KlineTimestamp to subtract.
        :return: A new KlineTimestamp if subtracting a timedelta, or a timedelta if subtracting another KlineTimestamp.
        :raises TypeError: If `other` is neither a timedelta nor a KlineTimestamp.
        """
        if isinstance(other, timedelta):
            new_timestamp_ms = self.timestamp_ms - int(other.total_seconds() * 1000)
            return KlineTimestamp(new_timestamp_ms, interval=self.interval, tzinfo=self.tzinfo)
        elif isinstance(other, KlineTimestamp):
            diff_ms = self.timestamp_ms - other.timestamp_ms
            return timedelta(milliseconds=diff_ms)
        else:
            raise TypeError(f"Unsupported type for -: 'KlineTimestamp' and '{type(other).__name__}'")

    def next(self) -> 'KlineTimestamp':
        """
        This method returns a new KlineTimestamp object representing the next candle (K-line).

        :return: A new KlineTimestamp object representing the next candle (K-line).
        """
        next_timestamp_ms = self.get_candle_open_timestamp_ms() + self.tick_ms
        return KlineTimestamp(next_timestamp_ms, interval=self.interval, tzinfo=self.tzinfo)

    def prev(self) -> 'KlineTimestamp':
        """
        This method returns a new KlineTimestamp object representing the previous candle (K-line).

        :return: A new KlineTimestamp object representing the previous candle (K-line).
        """
        prev_timestamp_ms = self.get_candle_open_timestamp_ms() - self.tick_ms
        return KlineTimestamp(prev_timestamp_ms, interval=self.interval, tzinfo=self.tzinfo)
       
    # Métodos de comparación
    def __eq__(self, other: 'KlineTimestamp') -> bool:
        """
        This method compares the current KlineTimestamp instance with another instance and returns True if they are equal, False otherwise.

        :param other: The instance to compare with the current instance. It must be an instance of the KlineTimestamp class.
        :type other: KlineTimestamp
        :return: True if the current instance is equal to the `other` instance, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        same_interval = self.interval == other.interval
        same_tzinfo = self.tzinfo == other.tzinfo
        same_timestamp = self.get_candle_open_timestamp_ms() == other.get_candle_open_timestamp_ms()
        return same_interval and same_tzinfo and same_timestamp

    def __lt__(self, other: 'KlineTimestamp') -> bool:
        """
        This method compares the current KlineTimestamp instance with another instance and returns True if the current instance is less than the `other` instance, False otherwise.

        :param other: The instance to compare with the current instance. It must be an instance of the KlineTimestamp class.
        :type other: KlineTimestamp
        :return: True if the current instance is less than the `other` instance, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.get_candle_open_timestamp_ms() < other.get_candle_open_timestamp_ms()

    def __le__(self, other: 'KlineTimestamp') -> bool:
        """
        This method compares the current KlineTimestamp instance with another instance and returns True if the current instance is less than or equal to the `other` instance, False otherwise.

        :param other: The instance to compare with the current instance. It must be an instance of the KlineTimestamp class.
        :type other: KlineTimestamp
        :return: True if the current instance is less than or equal to the `other` instance, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.get_candle_open_timestamp_ms() <= other.get_candle_open_timestamp_ms()

    def __gt__(self, other: 'KlineTimestamp') -> bool:
        """
        This method compares the current KlineTimestamp instance with another instance and returns True if the current instance is greater than the `other` instance, False otherwise.

        :param other: The instance to compare with the current instance. It must be an instance of the KlineTimestamp class.
        :type other: KlineTimestamp
        :return: True if the current instance is greater than the `other` instance, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.get_candle_open_timestamp_ms() > other.get_candle_open_timestamp_ms()

    def __ge__(self, other: 'KlineTimestamp') -> bool:
        """
        This method compares the current KlineTimestamp instance with another instance and returns True if the current instance is greater than or equal to the `other` instance, False otherwise.

        :param other: The instance to compare with the current instance. It must be an instance of the KlineTimestamp class.
        :type other: KlineTimestamp
        :return: True if the current instance is greater than or equal to the `other` instance, False otherwise.
        :rtype: bool
        """
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.get_candle_open_timestamp_ms() >= other.get_candle_open_timestamp_ms()

if __name__ == '__main__':
    from datetime import timedelta
    import pytz

    # Crear una instancia de KlineTimestamp
    kt = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='Europe/Madrid')

    # Probar get_candle_open_timestamp_ms
    open_ts_ms = kt.get_candle_open_timestamp_ms()
    print(f"Open timestamp (ms): {open_ts_ms}")

    # Probar get_candle_close_timestamp_ms
    close_ts_ms = kt.get_candle_close_timestamp_ms()
    print(f"Close timestamp (ms): {close_ts_ms}")

    # Probar to_datetime
    dt = kt.to_datetime()
    print(f"Datetime: {dt}")

    # Probar to_pandas_timestamp
    pd_ts = kt.to_pandas_timestamp()
    print(f"Pandas Timestamp: {pd_ts}")

    # Probar __str__ y __repr__
    print(f"String representation: {str(kt)}")
    print(f"Representation: {repr(kt)}")

    # Probar update_timezone
    kt.update_timezone('UTC')
    print(f"Updated timezone: {kt.tzinfo}")

    # Probar __add__
    kt_added = kt + timedelta(hours=1)
    print(f"Timestamp after adding 1 hour: {kt_added.to_datetime()}")

    # Probar __sub__ con timedelta
    kt_subtracted = kt - timedelta(hours=1)
    print(f"Timestamp after subtracting 1 hour: {kt_subtracted.to_datetime()}")

    # Probar __sub__ con otro KlineTimestamp
    kt_other = KlineTimestamp(timestamp_ms=1633033200000, interval='1h', tzinfo='UTC')
    time_diff = kt - kt_other
    print(f"Time difference between kt and kt_other: {time_diff}")

    # Probar next
    kt_next = kt.next()
    print(f"Next candle timestamp: {kt_next.to_datetime()}")

    # Probar prev
    kt_prev = kt.prev()
    print(f"Previous candle timestamp: {kt_prev.to_datetime()}")

    # Probar métodos de comparación
    print(f"kt == kt_other: {kt == kt_other}")
    print(f"kt > kt_other: {kt > kt_other}")
    print(f"kt < kt_other: {kt < kt_other}")
    print(f"kt >= kt_other: {kt >= kt_other}")
    print(f"kt <= kt_other: {kt <= kt_other}")

    # Probar igualdad con los mismos parámetros
    kt_same = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='UTC')
    print(f"kt == kt_same: {kt == kt_same}")

