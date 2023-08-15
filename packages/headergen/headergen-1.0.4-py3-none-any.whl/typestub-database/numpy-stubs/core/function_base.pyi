from numpy import ndarray as ndarray
from numpy.typing import ArrayLike as ArrayLike, DTypeLike as DTypeLike
from typing import Any, Tuple, overload
from typing_extensions import Literal as Literal, SupportsIndex

@overload
def linspace(start: _ArrayLikeNumber, stop: _ArrayLikeNumber, num: SupportsIndex = ..., endpoint: bool = ..., retstep: Literal[False] = ..., dtype: DTypeLike = ..., axis: SupportsIndex = ...) -> ndarray: ...
@overload
def linspace(start: _ArrayLikeNumber, stop: _ArrayLikeNumber, num: SupportsIndex = ..., endpoint: bool = ..., retstep: Literal[True] = ..., dtype: DTypeLike = ..., axis: SupportsIndex = ...) -> Tuple[ndarray, Any]: ...
def logspace(start: _ArrayLikeNumber, stop: _ArrayLikeNumber, num: SupportsIndex = ..., endpoint: bool = ..., base: _ArrayLikeNumber = ..., dtype: DTypeLike = ..., axis: SupportsIndex = ...) -> ndarray: ...
def geomspace(start: _ArrayLikeNumber, stop: _ArrayLikeNumber, num: SupportsIndex = ..., endpoint: bool = ..., dtype: DTypeLike = ..., axis: SupportsIndex = ...) -> ndarray: ...
