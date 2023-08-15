import enum
from tensorflow.python.framework import constant_op as constant_op, dtypes as dtypes, ops as ops, tensor_shape as tensor_shape
from tensorflow.python.ops import array_ops as array_ops, clip_ops as clip_ops, control_flow_ops as control_flow_ops, linalg_ops as linalg_ops, manip_ops as manip_ops, math_ops as math_ops, sort_ops as sort_ops
from tensorflow.python.ops.numpy_ops import np_arrays as np_arrays, np_dtypes as np_dtypes, np_export as np_export, np_utils as np_utils
from tensorflow.python.util import nest as nest
from typing import Any

newaxis: Any

def empty(shape, dtype=...): ...
def empty_like(a, dtype: Any | None = ...): ...
def zeros(shape, dtype=...): ...
def zeros_like(a, dtype: Any | None = ...): ...
def ones(shape, dtype=...): ...
def ones_like(a, dtype: Any | None = ...): ...
def eye(N, M: Any | None = ..., k: int = ..., dtype=...): ...
def identity(n, dtype=...): ...
def full(shape, fill_value, dtype: Any | None = ...): ...
def full_like(a, fill_value, dtype: Any | None = ..., order: str = ..., subok: bool = ..., shape: Any | None = ...): ...
def array(val, dtype: Any | None = ..., copy: bool = ..., ndmin: int = ...): ...
def asarray(a, dtype: Any | None = ...): ...
def asanyarray(a, dtype: Any | None = ...): ...
def ascontiguousarray(a, dtype: Any | None = ...): ...
def arange(start, stop: Any | None = ..., step: int = ..., dtype: Any | None = ...): ...
def diag(v, k: int = ...): ...
def diagonal(a, offset: int = ..., axis1: int = ..., axis2: int = ...): ...
def diagflat(v, k: int = ...): ...
def all(a, axis: Any | None = ..., keepdims: Any | None = ...): ...
def any(a, axis: Any | None = ..., keepdims: Any | None = ...): ...
def compress(condition, a, axis: Any | None = ...): ...
def copy(a): ...
def cumprod(a, axis: Any | None = ..., dtype: Any | None = ...): ...
def cumsum(a, axis: Any | None = ..., dtype: Any | None = ...): ...
def imag(val): ...
def size(x, axis: Any | None = ...): ...
def sum(a, axis: Any | None = ..., dtype: Any | None = ..., keepdims: Any | None = ...): ...
def prod(a, axis: Any | None = ..., dtype: Any | None = ..., keepdims: Any | None = ...): ...
def mean(a, axis: Any | None = ..., dtype: Any | None = ..., out: Any | None = ..., keepdims: Any | None = ...): ...
def amax(a, axis: Any | None = ..., out: Any | None = ..., keepdims: Any | None = ...): ...
def amin(a, axis: Any | None = ..., out: Any | None = ..., keepdims: Any | None = ...): ...
def var(a, axis: Any | None = ..., dtype: Any | None = ..., out: Any | None = ..., ddof: int = ..., keepdims: Any | None = ...): ...
def std(a, axis: Any | None = ..., keepdims: Any | None = ...): ...
def ravel(a): ...
def real(val): ...
def repeat(a, repeats, axis: Any | None = ...): ...
def around(a, decimals: int = ...): ...
def reshape(a, newshape, order: str = ...): ...
def expand_dims(a, axis): ...
def squeeze(a, axis: Any | None = ...): ...
def transpose(a, axes: Any | None = ...): ...
def swapaxes(a, axis1, axis2): ...
def moveaxis(a, source, destination): ...
def pad(array, pad_width, mode, **kwargs): ...
def take(a, indices, axis: Any | None = ..., out: Any | None = ..., mode: str = ...): ...
def where(condition, x: Any | None = ..., y: Any | None = ...): ...
def select(condlist, choicelist, default: int = ...): ...
def shape(a): ...
def ndim(a): ...
def isscalar(num): ...
def split(ary, indices_or_sections, axis: int = ...): ...

vsplit: Any
hsplit: Any
dsplit: Any

def broadcast_to(array, shape): ...
def stack(arrays, axis: int = ...): ...
def hstack(tup): ...
def vstack(tup): ...
def dstack(tup): ...
def atleast_1d(*arys): ...
def atleast_2d(*arys): ...
def atleast_3d(*arys): ...
def nonzero(a): ...
def diag_indices(n, ndim: int = ...): ...
def tri(N, M: Any | None = ..., k: int = ..., dtype: Any | None = ...): ...
def tril(m, k: int = ...): ...
def triu(m, k: int = ...): ...
def flip(m, axis: Any | None = ...): ...
def flipud(m): ...
def fliplr(m): ...
def roll(a, shift, axis: Any | None = ...): ...
def rot90(m, k: int = ..., axes=...): ...
def vander(x, N: Any | None = ..., increasing: bool = ...): ...
def ix_(*args): ...
def broadcast_arrays(*args, **kwargs): ...
def sign(x, out: Any | None = ..., where: Any | None = ..., **kwargs): ...
def take_along_axis(arr, indices, axis): ...

class _UpdateMethod(enum.Enum):
    UPDATE: int
    ADD: int
    MIN: int
    MAX: int
