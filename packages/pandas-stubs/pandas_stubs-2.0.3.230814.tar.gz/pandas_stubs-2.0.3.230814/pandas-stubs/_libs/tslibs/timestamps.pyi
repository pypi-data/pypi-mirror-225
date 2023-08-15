from datetime import (
    date as _date,
    datetime,
    time as _time,
    timedelta,
    tzinfo as _tzinfo,
)
import sys
from time import struct_time
from typing import (
    ClassVar,
    Literal,
    overload,
)

import numpy as np
from pandas import (
    DatetimeIndex,
    Index,
    TimedeltaIndex,
)
from pandas.core.series import (
    Series,
    TimedeltaSeries,
    TimestampSeries,
)
from typing_extensions import (
    Never,
    Self,
    TypeAlias,
)

from pandas._libs.tslibs import (
    BaseOffset,
    Period,
    Tick,
    Timedelta,
)
from pandas._typing import (
    np_ndarray_bool,
    npt,
)

_Ambiguous: TypeAlias = bool | Literal["raise", "NaT"]
_Nonexistent: TypeAlias = (
    Literal["raise", "NaT", "shift_backward", "shift_forward"] | Timedelta | timedelta
)

if sys.version_info >= (3, 9):
    from datetime import _IsoCalendarDate
else:
    _IsoCalendarDate: TypeAlias = tuple[int, int, int]

class Timestamp(datetime):
    min: ClassVar[Timestamp]
    max: ClassVar[Timestamp]

    resolution: ClassVar[Timedelta]
    value: int
    def __new__(
        cls,
        ts_input: np.integer | float | str | _date | datetime | np.datetime64 = ...,
        # Freq is deprecated but is left in to allow code like Timestamp(2000,1,1)
        # Removing it would make the other arguments position only
        freq: int | str | BaseOffset | None = ...,
        tz: str | _tzinfo | int | None = ...,
        unit: str | int | None = ...,
        year: int | None = ...,
        month: int | None = ...,
        day: int | None = ...,
        hour: int | None = ...,
        minute: int | None = ...,
        second: int | None = ...,
        microsecond: int | None = ...,
        nanosecond: int | None = ...,
        tzinfo: _tzinfo | None = ...,
        *,
        fold: Literal[0, 1] | None = ...,
    ) -> Self: ...
    # GH 46171
    # While Timestamp can return pd.NaT, having the constructor return
    # a Union with NaTType makes things awkward for users of pandas
    @property
    def year(self) -> int: ...
    @property
    def month(self) -> int: ...
    @property
    def day(self) -> int: ...
    @property
    def hour(self) -> int: ...
    @property
    def minute(self) -> int: ...
    @property
    def second(self) -> int: ...
    @property
    def microsecond(self) -> int: ...
    @property
    def nanosecond(self) -> int: ...
    @property
    def tzinfo(self) -> _tzinfo | None: ...
    @property
    def tz(self) -> _tzinfo | None: ...
    @property
    def fold(self) -> int: ...
    @classmethod
    def fromtimestamp(cls, t: float, tz: _tzinfo | str | None = ...) -> Self: ...
    @classmethod
    def utcfromtimestamp(cls, ts: float) -> Self: ...
    @classmethod
    def today(cls, tz: _tzinfo | str | None = ...) -> Self: ...
    @classmethod
    def fromordinal(
        cls,
        ordinal: int,
        # freq produces a FutureWarning about being deprecated in a future version
        freq: None = ...,
        tz: _tzinfo | str | None = ...,
    ) -> Self: ...
    @classmethod
    def now(cls, tz: _tzinfo | str | None = ...) -> Self: ...
    @classmethod
    def utcnow(cls) -> Self: ...
    # error: Signature of "combine" incompatible with supertype "datetime"
    @classmethod
    def combine(cls, date: _date, time: _time) -> datetime: ...  # type: ignore[override]
    @classmethod
    def fromisoformat(cls, date_string: str) -> Self: ...
    def strftime(self, format: str) -> str: ...
    def __format__(self, fmt: str) -> str: ...
    def toordinal(self) -> int: ...
    def timetuple(self) -> struct_time: ...
    def timestamp(self) -> float: ...
    def utctimetuple(self) -> struct_time: ...
    def date(self) -> _date: ...
    def time(self) -> _time: ...
    def timetz(self) -> _time: ...
    # Override since fold is more precise than datetime.replace(fold:int)
    # Here it is restricted to be 0 or 1 using a Literal
    # Violation of Liskov substitution principle
    def replace(  # type:ignore[override]
        self,
        year: int | None = ...,
        month: int | None = ...,
        day: int | None = ...,
        hour: int | None = ...,
        minute: int | None = ...,
        second: int | None = ...,
        microsecond: int | None = ...,
        tzinfo: _tzinfo | None = ...,
        fold: Literal[0, 1] | None = ...,
    ) -> Timestamp: ...
    def astimezone(self, tz: _tzinfo | None = ...) -> Self: ...
    def ctime(self) -> str: ...
    def isoformat(self, sep: str = ..., timespec: str = ...) -> str: ...
    @classmethod
    def strptime(cls, date_string: Never, format: Never) -> Never: ...  # type: ignore[override]
    def utcoffset(self) -> timedelta | None: ...
    def tzname(self) -> str | None: ...
    def dst(self) -> timedelta | None: ...
    # Mypy complains Forward operator "<inequality op>" is not callable, so ignore misc
    # for le, lt ge and gt
    @overload  # type: ignore[override]
    def __le__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc]
    @overload
    def __le__(self, other: Index | npt.NDArray[np.datetime64]) -> np_ndarray_bool: ...
    @overload
    def __le__(self, other: TimestampSeries) -> Series[bool]: ...
    @overload  # type: ignore[override]
    def __lt__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc]
    @overload
    def __lt__(self, other: Index | npt.NDArray[np.datetime64]) -> np_ndarray_bool: ...
    @overload
    def __lt__(self, other: TimestampSeries) -> Series[bool]: ...
    @overload  # type: ignore[override]
    def __ge__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc]
    @overload
    def __ge__(self, other: Index | npt.NDArray[np.datetime64]) -> np_ndarray_bool: ...
    @overload
    def __ge__(self, other: TimestampSeries) -> Series[bool]: ...
    @overload  # type: ignore[override]
    def __gt__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc]
    @overload
    def __gt__(self, other: Index | npt.NDArray[np.datetime64]) -> np_ndarray_bool: ...
    @overload
    def __gt__(self, other: TimestampSeries) -> Series[bool]: ...
    # error: Signature of "__add__" incompatible with supertype "date"/"datetime"
    @overload  # type: ignore[override]
    def __add__(
        self, other: npt.NDArray[np.timedelta64]
    ) -> npt.NDArray[np.datetime64]: ...
    @overload
    def __add__(self, other: timedelta | np.timedelta64 | Tick) -> Self: ...
    @overload
    def __add__(self, other: TimedeltaSeries) -> TimestampSeries: ...
    @overload
    def __add__(self, other: TimedeltaIndex) -> DatetimeIndex: ...
    @overload
    def __radd__(self, other: timedelta) -> Self: ...
    @overload
    def __radd__(self, other: TimedeltaIndex) -> DatetimeIndex: ...
    @overload
    def __radd__(
        self, other: npt.NDArray[np.timedelta64]
    ) -> npt.NDArray[np.datetime64]: ...
    # TODO: test dt64
    @overload  # type: ignore[override]
    def __sub__(self, other: Timestamp | datetime | np.datetime64) -> Timedelta: ...
    @overload
    def __sub__(self, other: timedelta | np.timedelta64 | Tick) -> Self: ...
    @overload
    def __sub__(self, other: TimedeltaIndex) -> DatetimeIndex: ...
    @overload
    def __sub__(self, other: TimedeltaSeries) -> TimestampSeries: ...
    @overload
    def __sub__(
        self, other: npt.NDArray[np.timedelta64]
    ) -> npt.NDArray[np.datetime64]: ...
    @overload
    def __eq__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc] # pyright: ignore[reportOverlappingOverload]
    @overload
    def __eq__(self, other: TimestampSeries) -> Series[bool]: ...  # type: ignore[misc]
    @overload
    def __eq__(self, other: npt.NDArray[np.datetime64] | Index) -> np_ndarray_bool: ...  # type: ignore[misc]
    @overload
    def __eq__(self, other: object) -> Literal[False]: ...
    @overload
    def __ne__(self, other: Timestamp | datetime | np.datetime64) -> bool: ...  # type: ignore[misc] # pyright: ignore[reportOverlappingOverload]
    @overload
    def __ne__(self, other: TimestampSeries) -> Series[bool]: ...  # type: ignore[misc]
    @overload
    def __ne__(self, other: npt.NDArray[np.datetime64] | Index) -> np_ndarray_bool: ...  # type: ignore[misc]
    @overload
    def __ne__(self, other: object) -> Literal[True]: ...
    def __hash__(self) -> int: ...
    def weekday(self) -> int: ...
    def isoweekday(self) -> int: ...
    def isocalendar(self) -> _IsoCalendarDate: ...
    @property
    def is_leap_year(self) -> bool: ...
    @property
    def is_month_start(self) -> bool: ...
    @property
    def is_quarter_start(self) -> bool: ...
    @property
    def is_year_start(self) -> bool: ...
    @property
    def is_month_end(self) -> bool: ...
    @property
    def is_quarter_end(self) -> bool: ...
    @property
    def is_year_end(self) -> bool: ...
    def to_pydatetime(self, warn: bool = ...) -> datetime: ...
    def to_datetime64(self) -> np.datetime64: ...
    def to_period(self, freq: BaseOffset | str | None = ...) -> Period: ...
    def to_julian_date(self) -> np.float64: ...
    @property
    def asm8(self) -> np.datetime64: ...
    def tz_convert(self, tz: _tzinfo | str | None) -> Self: ...
    # TODO: could return NaT?
    def tz_localize(
        self,
        tz: _tzinfo | str | None,
        ambiguous: _Ambiguous = ...,
        nonexistent: _Nonexistent = ...,
    ) -> Self: ...
    def normalize(self) -> Self: ...
    # TODO: round/floor/ceil could return NaT?
    def round(
        self,
        freq: str,
        ambiguous: _Ambiguous = ...,
        nonexistent: _Nonexistent = ...,
    ) -> Self: ...
    def floor(
        self,
        freq: str,
        ambiguous: _Ambiguous = ...,
        nonexistent: _Nonexistent = ...,
    ) -> Self: ...
    def ceil(
        self,
        freq: str,
        ambiguous: _Ambiguous = ...,
        nonexistent: _Nonexistent = ...,
    ) -> Self: ...
    def day_name(self, locale: str | None = ...) -> str: ...
    def month_name(self, locale: str | None = ...) -> str: ...
    @property
    def day_of_week(self) -> int: ...
    @property
    def dayofweek(self) -> int: ...
    @property
    def day_of_year(self) -> int: ...
    @property
    def dayofyear(self) -> int: ...
    @property
    def weekofyear(self) -> int: ...
    @property
    def quarter(self) -> int: ...
    @property
    def week(self) -> int: ...
    def to_numpy(self) -> np.datetime64: ...
    @property
    def days_in_month(self) -> int: ...
    @property
    def daysinmonth(self) -> int: ...
