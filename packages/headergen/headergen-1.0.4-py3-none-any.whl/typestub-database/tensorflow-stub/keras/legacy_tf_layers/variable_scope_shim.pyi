from tensorflow.python.eager import context as context
from tensorflow.python.framework import dtypes as dtypes, ops as ops, tensor_shape as tensor_shape
from tensorflow.python.keras.engine import base_layer as base_layer
from tensorflow.python.keras.utils import tf_contextlib as tf_contextlib, tf_inspect as tf_inspect
from tensorflow.python.module import module as module
from tensorflow.python.ops import init_ops as init_ops, variables as variables
from tensorflow.python.util import tf_decorator as tf_decorator
from typing import Any

def as_shape(shape): ...
def fn_args(fn): ...
def validate_synchronization_aggregation_trainable(synchronization, aggregation, trainable, name): ...

class _EagerVariableStore:
    def __init__(self) -> None: ...
    def get_variable(self, name, shape: Any | None = ..., dtype=..., initializer: Any | None = ..., regularizer: Any | None = ..., reuse: Any | None = ..., trainable: Any | None = ..., collections: Any | None = ..., caching_device: Any | None = ..., partitioner: Any | None = ..., validate_shape: bool = ..., use_resource: Any | None = ..., custom_getter: Any | None = ..., constraint: Any | None = ..., synchronization=..., aggregation=...): ...
    def add_regularizer(self, var, regularizer) -> None: ...

class VariableAndLossTracker(module.Module):
    def __init__(self) -> None: ...
    def scope(self) -> None: ...
    def get_regularization_losses(self): ...

class VariableScopeWrapperLayer(base_layer.Layer):
    tracker: Any
    def __init__(self, **kwargs) -> None: ...
    def forward_pass(self, *args, **kwargs) -> None: ...
    def call(self, *args, **kwargs): ...
