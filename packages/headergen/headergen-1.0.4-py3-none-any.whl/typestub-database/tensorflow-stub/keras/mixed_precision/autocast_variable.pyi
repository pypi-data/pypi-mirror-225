from tensorflow.python.eager import context as context
from tensorflow.python.framework import ops as ops
from tensorflow.python.keras.distribute import distributed_training_utils as distributed_training_utils
from tensorflow.python.ops import math_ops as math_ops, resource_variable_ops as resource_variable_ops, variables as variables
from tensorflow.python.types import core as core
from typing import Any

def numpy_text(tensor, is_repr: bool = ...): ...

class AutoCastVariable(variables.Variable, core.Tensor):
    def __init__(self, variable) -> None: ...
    @property
    def dtype(self): ...
    @property
    def true_dtype(self): ...
    def value(self): ...
    def read_value(self): ...
    def sparse_read(self, indices, name: Any | None = ...): ...
    def gather_nd(self, indices, name: Any | None = ...): ...
    def __getattr__(self, name): ...
    def set_shape(self, shape): ...
    @property
    def trainable(self): ...
    @property
    def synchronization(self): ...
    @property
    def aggregation(self): ...
    def eval(self, session: Any | None = ...): ...
    def initialized_value(self): ...
    @property
    def initial_value(self): ...
    @property
    def constraint(self): ...
    def assign(self, value, use_locking: Any | None = ..., name: Any | None = ..., read_value: bool = ...): ...
    def assign_add(self, delta, use_locking: Any | None = ..., name: Any | None = ..., read_value: bool = ...): ...
    def assign_sub(self, delta, use_locking: Any | None = ..., name: Any | None = ..., read_value: bool = ...): ...
    def scatter_sub(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_add(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_max(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_min(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_mul(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_div(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_update(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def batch_scatter_update(self, sparse_delta, use_locking: bool = ..., name: Any | None = ...): ...
    def scatter_nd_sub(self, indices, updates, name: Any | None = ...): ...
    def scatter_nd_add(self, indices, updates, name: Any | None = ...): ...
    def scatter_nd_update(self, indices, updates, name: Any | None = ...): ...
    def load(self, value, session: Any | None = ...): ...
    @property
    def name(self): ...
    @property
    def initializer(self): ...
    @property
    def device(self): ...
    @property
    def op(self): ...
    @property
    def graph(self): ...
    @property
    def shape(self): ...
    def get_shape(self): ...
    def to_proto(self, export_scope: Any | None = ...): ...
    def from_proto(self, variable_def, import_scope: Any | None = ...): ...
    def __add__(self, o): ...
    def __radd__(self, o): ...
    def __sub__(self, o): ...
    def __rsub__(self, o): ...
    def __mul__(self, o): ...
    def __rmul__(self, o): ...
    def __truediv__(self, o): ...
    def __rtruediv__(self, o): ...
    def __floordiv__(self, o): ...
    def __rfloordiv__(self, o): ...
    def __mod__(self, o): ...
    def __rmod__(self, o): ...
    def __lt__(self, o): ...
    def __le__(self, o): ...
    def __gt__(self, o): ...
    def __ge__(self, o): ...
    def __getitem__(self, o): ...
    def __pow__(self, o, modulo: Any | None = ...): ...
    def __rpow__(self, o): ...
    def __neg__(self): ...
    def __abs__(self): ...
    def __div__(self, o): ...
    def __rdiv__(self, o): ...
    def __matmul__(self, o): ...
    def __rmatmul__(self, o): ...

def create_autocast_variable(variable): ...

class enable_auto_cast_variables:
    def __init__(self, dtype) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, type_arg, value_arg, traceback_arg) -> None: ...
