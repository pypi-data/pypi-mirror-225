from tensorflow.python.framework import ops as ops
from tensorflow.python.ops import list_ops as list_ops, tensor_array_ops as tensor_array_ops
from typing import Any

def dynamic_list_append(target, element): ...

class TensorList:
    dtype: Any
    shape: Any
    def __init__(self, shape, dtype) -> None: ...
    list_: Any
    def append(self, value) -> None: ...
    def pop(self): ...
    def clear(self) -> None: ...
    def count(self): ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, value) -> None: ...
