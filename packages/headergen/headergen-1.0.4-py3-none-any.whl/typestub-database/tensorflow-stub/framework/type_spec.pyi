import abc
from tensorflow.python.framework import composite_tensor as composite_tensor, dtypes as dtypes, tensor_shape as tensor_shape
from tensorflow.python.util import compat as compat, nest as nest, tf_decorator as tf_decorator
from tensorflow.python.util.lazy_loader import LazyLoader as LazyLoader
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

tensor_spec: Any
ops: Any

class TypeSpec(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def value_type(self): ...
    def is_compatible_with(self, spec_or_value): ...
    def most_specific_compatible_type(self, other: TypeSpec) -> TypeSpec: ...
    def __eq__(self, other) -> bool: ...
    def __ne__(self, other) -> bool: ...
    def __hash__(self) -> int: ...
    def __reduce__(self): ...

class TypeSpecBatchEncoder(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def batch(self, spec, batch_size): ...
    @abc.abstractmethod
    def unbatch(self, spec): ...
    @abc.abstractmethod
    def encode(self, spec, value, minimum_rank: int = ...): ...
    @abc.abstractmethod
    def decode(self, spec, encoded_value): ...
    @abc.abstractmethod
    def encoding_specs(self, spec): ...

class LegacyTypeSpecBatchEncoder(TypeSpecBatchEncoder):
    def batch(self, type_spec, batch_size): ...
    def unbatch(self, type_spec): ...
    def encode(self, type_spec, value, minimum_rank: int = ...): ...
    def decode(self, type_spec, encoded_value): ...
    def encoding_specs(self, spec): ...

class BatchableTypeSpec(TypeSpec, metaclass=abc.ABCMeta):
    __batch_encoder__: Any

def get_batchable_flat_tensor_specs(spec, context_spec: Any | None = ...): ...
def batchable_to_tensor_list(spec, value, minimum_rank: int = ...): ...
def batchable_from_tensor_list(spec, tensor_list): ...
def type_spec_from_value(value) -> TypeSpec: ...
def register_type_spec_from_value_converter(type_object, converter_fn, allow_subclass: bool = ...) -> None: ...
def register(name): ...
def get_name(cls): ...
def lookup(name): ...
