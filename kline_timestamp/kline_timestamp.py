from dataclasses import dataclass, field
from typing import Union
from datetime import datetime, timedelta, timezone
import pytz
import pandas as pd


@dataclass(frozen=True)
class KlineTimestamp:
    timestamp_ms: int
    interval: str
    tzinfo: Union[pytz.BaseTzInfo, str] = 'UTC'
    open: int = field(init=False)
    close: int = field(init=False)

    # Definición de tick_milliseconds como campo de clase
    tick_milliseconds: dict = field(default_factory=lambda: {
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
    }, init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, 'interval', self.interval.lower())
        if self.interval not in self.tick_milliseconds:
            raise ValueError(f"Invalid interval: {self.interval}. Valid intervals are: {list(self.tick_milliseconds.keys())}.")

        tick_ms = self.tick_milliseconds[self.interval]
        open_ts = (self.timestamp_ms // tick_ms) * tick_ms
        close_ts = open_ts + tick_ms - 1
        object.__setattr__(self, 'tick_ms', tick_ms)
        object.__setattr__(self, 'open', open_ts)
        object.__setattr__(self, 'close', close_ts)

        if isinstance(self.tzinfo, str):
            tz = pytz.timezone(self.tzinfo)
        elif isinstance(self.tzinfo, pytz.BaseTzInfo):
            tz = self.tzinfo
        else:
            raise TypeError("tzinfo must be a string or pytz.timezone object")
        object.__setattr__(self, 'tzinfo', tz)

    def to_datetime(self) -> datetime:
        """
        Retorna el objeto datetime en la zona horaria proporcionada.
        """
        dt_utc = datetime.fromtimestamp(self.open / 1000, tz=timezone.utc)
        dt_local = dt_utc.astimezone(self.tzinfo)
        return dt_local

    def to_pandas_timestamp(self) -> pd.Timestamp:
        """
        Retorna un objeto pandas.Timestamp en la zona horaria proporcionada.
        """
        return pd.Timestamp(self.open, unit='ms', tz='UTC').tz_convert(self.tzinfo)

    def with_timezone(self, tzinfo: Union[str, pytz.BaseTzInfo]) -> 'KlineTimestamp':
        """
        Devuelve una nueva instancia de KlineTimestamp con una zona horaria actualizada.
        """
        return KlineTimestamp(self.timestamp_ms, self.interval, tzinfo)

    def __str__(self):
        return f"KlineTimestamp({self.to_datetime().isoformat()}, interval='{self.interval}', tz='{self.tzinfo.zone}')"

    def __eq__(self, other: 'KlineTimestamp') -> bool:
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.open == other.open

    def __lt__(self, other: 'KlineTimestamp') -> bool:
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.open < other.open

    def __le__(self, other: 'KlineTimestamp') -> bool:
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.open <= other.open

    def __gt__(self, other: 'KlineTimestamp') -> bool:
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.open > other.open

    def __ge__(self, other: 'KlineTimestamp') -> bool:
        if not isinstance(other, KlineTimestamp):
            return NotImplemented
        return self.open >= other.open

    def __add__(self, other: timedelta) -> 'KlineTimestamp':
        if not isinstance(other, timedelta):
            raise TypeError(f"Unsupported type for +: 'KlineTimestamp' and '{type(other).__name__}'")
        new_timestamp_ms = self.timestamp_ms + int(other.total_seconds() * 1000)
        return KlineTimestamp(new_timestamp_ms, self.interval, self.tzinfo)

    def __sub__(self, other: Union[timedelta, 'KlineTimestamp']) -> Union['KlineTimestamp', timedelta]:
        if isinstance(other, timedelta):
            new_timestamp_ms = self.timestamp_ms - int(other.total_seconds() * 1000)
            return KlineTimestamp(new_timestamp_ms, self.interval, self.tzinfo)
        elif isinstance(other, KlineTimestamp):
            return timedelta(milliseconds=self.timestamp_ms - other.timestamp_ms)
        else:
            raise TypeError(f"Unsupported type for -: 'KlineTimestamp' and '{type(other).__name__}'")

    def next(self) -> 'KlineTimestamp':
        """
        Retorna el siguiente KlineTimestamp.
        """
        next_timestamp_ms = self.open + self.tick_ms
        return KlineTimestamp(next_timestamp_ms, self.interval, self.tzinfo)

    def prev(self) -> 'KlineTimestamp':
        """
        Retorna el KlineTimestamp anterior.
        """
        prev_timestamp_ms = self.open - self.tick_ms
        return KlineTimestamp(prev_timestamp_ms, self.interval, self.tzinfo)

    # Métodos de comparación ya están manejados por @dataclass


if __name__ == '__main__':
    from datetime import timedelta
    import pytz

    # Crear una instancia de kline_timestamp
    kt = KlineTimestamp(timestamp_ms=1633036800000, interval='1h', tzinfo='Europe/Madrid')

    # Probar get_candle_open_timestamp_ms
    open_ts_ms = kt.open
    print(f"Open timestamp (ms): {open_ts_ms}")

    # Probar get_candle_close_timestamp_ms
    close_ts_ms = kt.close
    print(f"Close timestamp (ms): {close_ts_ms}")

    # open and close as attributes
    print(f"Open as attribute: {kt.open}")
    print(f"Close as attribute: {kt.close}")

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
    kt_utc = kt.with_timezone('UTC')
    print(f"Updated timezone: {kt_utc.tzinfo}")
    print(kt_utc)
    # Probar __add__
    kt_added = kt + timedelta(hours=1)
    print(f"Timestamp after adding 1 hour: {kt_added.to_datetime()}")

    # Probar __sub__ con timedelta
    kt_subtracted = kt - timedelta(hours=1)
    print(f"Timestamp after subtracting 1 hour: {kt_subtracted.to_datetime()}")

    # Probar __sub__ con otro kline_timestamp
    kt_other = KlineTimestamp(timestamp_ms=1633033200000, interval='1h', tzinfo='UTC')
    time_diff = kt - kt_other
    print(f"Time difference between kt and kt_other{kt_other}: \n{time_diff}")

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
