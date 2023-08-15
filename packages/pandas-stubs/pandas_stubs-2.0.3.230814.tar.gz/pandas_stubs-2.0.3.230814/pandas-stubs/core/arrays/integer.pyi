from pandas.core.arrays.masked import BaseMaskedArray

from pandas._libs.missing import NAType

from pandas.core.dtypes.base import ExtensionDtype as ExtensionDtype

class _IntegerDtype(ExtensionDtype):
    base: None
    @property
    def na_value(self) -> NAType: ...
    @property
    def itemsize(self) -> int: ...
    @classmethod
    def construct_array_type(cls) -> type[IntegerArray]: ...

class IntegerArray(BaseMaskedArray):
    def dtype(self): ...
    def __init__(self, values, mask, copy: bool = ...) -> None: ...
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs): ...
    def __setitem__(self, key, value) -> None: ...
    def astype(self, dtype, copy: bool = ...): ...

class Int8Dtype(_IntegerDtype): ...
class Int16Dtype(_IntegerDtype): ...
class Int32Dtype(_IntegerDtype): ...
class Int64Dtype(_IntegerDtype): ...
class UInt8Dtype(_IntegerDtype): ...
class UInt16Dtype(_IntegerDtype): ...
class UInt32Dtype(_IntegerDtype): ...
class UInt64Dtype(_IntegerDtype): ...
