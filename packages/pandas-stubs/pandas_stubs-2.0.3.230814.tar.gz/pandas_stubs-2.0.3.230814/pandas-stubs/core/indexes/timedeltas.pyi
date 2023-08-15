from collections.abc import (
    Hashable,
    Sequence,
)
import datetime as dt
from typing import (
    Literal,
    overload,
)

import numpy as np
from pandas import (
    DateOffset,
    Period,
)
from pandas.core.indexes.accessors import TimedeltaIndexProperties
from pandas.core.indexes.datetimelike import DatetimeTimedeltaMixin
from pandas.core.indexes.datetimes import DatetimeIndex
from pandas.core.indexes.period import PeriodIndex
from pandas.core.series import TimedeltaSeries
from typing_extensions import Self

from pandas._libs import (
    Timedelta,
    Timestamp,
)
from pandas._libs.tslibs import BaseOffset
from pandas._typing import (
    AnyArrayLike,
    TimedeltaConvertibleTypes,
    num,
)

class TimedeltaIndex(DatetimeTimedeltaMixin[Timedelta], TimedeltaIndexProperties):
    def __new__(
        cls,
        data: AnyArrayLike
        | list[str]
        | Sequence[dt.timedelta | Timedelta | np.timedelta64 | float] = ...,
        unit: Literal["D", "h", "m", "s", "ms", "us", "ns"] = ...,
        freq: str | BaseOffset = ...,
        closed: object = ...,
        dtype: Literal["<m8[ns]"] = ...,
        copy: bool = ...,
        name: str = ...,
    ) -> Self: ...
    # various ignores needed for mypy, as we do want to restrict what can be used in
    # arithmetic for these types
    @overload
    def __add__(self, other: Period) -> PeriodIndex: ...
    @overload
    def __add__(self, other: DatetimeIndex) -> DatetimeIndex: ...
    @overload
    def __add__(self, other: Timedelta | Self) -> Self: ...
    def __radd__(self, other: Timestamp | DatetimeIndex) -> DatetimeIndex: ...  # type: ignore[override]
    def __sub__(self, other: Timedelta | Self) -> Self: ...
    def __mul__(self, other: num) -> Self: ...
    def __truediv__(self, other: num) -> Self: ...
    def astype(self, dtype, copy: bool = ...): ...
    def get_value(self, series, key): ...
    def get_loc(self, key, tolerance=...): ...
    def searchsorted(self, value, side: str = ..., sorter=...): ...
    @property
    def inferred_type(self) -> str: ...
    def insert(self, loc, item): ...
    def to_series(self, index=..., name=...) -> TimedeltaSeries: ...

def timedelta_range(
    start: TimedeltaConvertibleTypes = ...,
    end: TimedeltaConvertibleTypes = ...,
    periods: int | None = ...,
    freq: str | DateOffset | Timedelta | dt.timedelta | None = ...,
    name: Hashable | None = ...,
    closed: Literal["left", "right"] | None = ...,
) -> TimedeltaIndex: ...
