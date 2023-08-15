from absl.flags import *
from tensorflow.python.util import tf_decorator as tf_decorator
from typing import Any

class _FlagValuesWrapper:
    def __init__(self, flags_object) -> None: ...
    def __getattribute__(self, name): ...
    def __getattr__(self, name): ...
    def __setattr__(self, name, value): ...
    def __delattr__(self, name): ...
    def __dir__(self): ...
    def __getitem__(self, name): ...
    def __setitem__(self, name, flag): ...
    def __len__(self): ...
    def __iter__(self): ...
    def __call__(self, *args, **kwargs): ...

DEFINE_string: Any
DEFINE_boolean: Any
DEFINE_bool = DEFINE_boolean
DEFINE_float: Any
DEFINE_integer: Any
FLAGS: Any
