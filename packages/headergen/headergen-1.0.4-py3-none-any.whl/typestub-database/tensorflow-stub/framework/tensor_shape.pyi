from tensorflow.core.framework import tensor_shape_pb2 as tensor_shape_pb2
from tensorflow.python import tf2 as tf2
from tensorflow.python.eager import monitoring as monitoring
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def enable_v2_tensorshape() -> None: ...
def disable_v2_tensorshape() -> None: ...
def dimension_value(dimension): ...
def dimension_at_index(shape, index): ...

class Dimension:
    def __init__(self, value) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __bool__(self): ...
    def __int__(self): ...
    def __long__(self): ...
    def __index__(self): ...
    @property
    def value(self): ...
    def is_compatible_with(self, other): ...
    def assert_is_compatible_with(self, other) -> None: ...
    def merge_with(self, other): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...
    def __sub__(self, other): ...
    def __rsub__(self, other): ...
    def __mul__(self, other): ...
    def __rmul__(self, other): ...
    def __floordiv__(self, other): ...
    def __rfloordiv__(self, other): ...
    def __div__(self, other): ...
    def __rdiv__(self, other) -> None: ...
    def __truediv__(self, other) -> None: ...
    def __rtruediv__(self, other) -> None: ...
    def __mod__(self, other): ...
    def __rmod__(self, other): ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...
    def __reduce__(self): ...

def as_dimension(value): ...

class TensorShape:
    def __init__(self, dims) -> None: ...
    @property
    def rank(self): ...
    @property
    def dims(self): ...
    @property
    def ndims(self): ...
    def __len__(self): ...
    def __bool__(self): ...
    __nonzero__: Any
    def __iter__(self): ...
    def __getitem__(self, key): ...
    def num_elements(self): ...
    def merge_with(self, other): ...
    def __add__(self, other): ...
    def __radd__(self, other): ...
    def concatenate(self, other): ...
    def assert_same_rank(self, other) -> None: ...
    def assert_has_rank(self, rank) -> None: ...
    def with_rank(self, rank): ...
    def with_rank_at_least(self, rank): ...
    def with_rank_at_most(self, rank): ...
    def is_compatible_with(self, other): ...
    def assert_is_compatible_with(self, other) -> None: ...
    def most_specific_compatible_shape(self, other): ...
    def is_fully_defined(self): ...
    def assert_is_fully_defined(self) -> None: ...
    def as_list(self): ...
    def as_proto(self): ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __reduce__(self): ...
    def __concat__(self, other): ...

def as_shape(shape): ...
def unknown_shape(rank: Any | None = ..., **kwargs): ...
