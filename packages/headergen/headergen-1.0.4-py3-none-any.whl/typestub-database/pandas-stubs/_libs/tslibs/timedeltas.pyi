import numpy as np
from datetime import timedelta
from pandas._libs.tslibs import NaTType as NaTType, Tick as Tick
from pandas._typing import npt as npt
from typing import Union, ClassVar, overload

def ints_to_pytimedelta(arr: npt.NDArray[np.int64], box: bool = ...) -> npt.NDArray[np.object_]: ...
def array_to_timedelta64(values: npt.NDArray[np.object_], unit: Union[str, None] = ..., errors: str = ...) -> np.ndarray: ...
def parse_timedelta_unit(unit: Union[str, None]) -> str: ...
def delta_to_nanoseconds(delta: Union[Tick, np.timedelta64, timedelta, int]) -> int: ...

class Timedelta(timedelta):
    min: ClassVar[Timedelta]
    max: ClassVar[Timedelta]
    resolution: ClassVar[Timedelta]
    value: int
    def __new__(cls, value=..., unit: str = ..., **kwargs: Union[int, float, np.integer, np.floating]) -> Union[_S, NaTType]: ...
    @property
    def days(self) -> int: ...
    @property
    def seconds(self) -> int: ...
    @property
    def microseconds(self) -> int: ...
    def total_seconds(self) -> float: ...
    def to_pytimedelta(self) -> timedelta: ...
    def to_timedelta64(self) -> np.timedelta64: ...
    @property
    def asm8(self) -> np.timedelta64: ...
    def round(self, freq: str) -> _S: ...
    def floor(self, freq: str) -> _S: ...
    def ceil(self, freq: str) -> _S: ...
    @property
    def resolution_string(self) -> str: ...
    def __add__(self, other: timedelta) -> timedelta: ...
    def __radd__(self, other: timedelta) -> timedelta: ...
    def __sub__(self, other: timedelta) -> timedelta: ...
    def __rsub__(self, other: timedelta) -> timedelta: ...
    def __neg__(self) -> timedelta: ...
    def __pos__(self) -> timedelta: ...
    def __abs__(self) -> timedelta: ...
    def __mul__(self, other: float) -> timedelta: ...
    def __rmul__(self, other: float) -> timedelta: ...
    @overload
    def __floordiv__(self, other: timedelta) -> int: ...
    @overload
    def __floordiv__(self, other: int) -> timedelta: ...
    @overload
    def __truediv__(self, other: timedelta) -> float: ...
    @overload
    def __truediv__(self, other: float) -> timedelta: ...
    def __mod__(self, other: timedelta) -> timedelta: ...
    def __divmod__(self, other: timedelta) -> tuple[int, timedelta]: ...
    def __le__(self, other: timedelta) -> bool: ...
    def __lt__(self, other: timedelta) -> bool: ...
    def __ge__(self, other: timedelta) -> bool: ...
    def __gt__(self, other: timedelta) -> bool: ...
    def __hash__(self) -> int: ...
