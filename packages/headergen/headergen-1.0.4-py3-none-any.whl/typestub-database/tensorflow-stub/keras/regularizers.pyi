from tensorflow.python.keras import backend as backend
from tensorflow.python.keras.utils.generic_utils import deserialize_keras_object as deserialize_keras_object, serialize_keras_object as serialize_keras_object
from tensorflow.python.ops import math_ops as math_ops
from tensorflow.python.util.tf_export import keras_export as keras_export
from typing import Any

class Regularizer:
    def __call__(self, x): ...
    @classmethod
    def from_config(cls, config): ...
    def get_config(self) -> None: ...

class L1L2(Regularizer):
    l1: Any
    l2: Any
    def __init__(self, l1: float = ..., l2: float = ...) -> None: ...
    def __call__(self, x): ...
    def get_config(self): ...

class L1(Regularizer):
    l1: Any
    def __init__(self, l1: float = ..., **kwargs) -> None: ...
    def __call__(self, x): ...
    def get_config(self): ...

class L2(Regularizer):
    l2: Any
    def __init__(self, l2: float = ..., **kwargs) -> None: ...
    def __call__(self, x): ...
    def get_config(self): ...

def l1_l2(l1: float = ..., l2: float = ...): ...
l1 = L1
l2 = L2

def serialize(regularizer): ...
def deserialize(config, custom_objects: Any | None = ...): ...
def get(identifier): ...
