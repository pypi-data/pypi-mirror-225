from tensorflow.python.data.util import nest as nest
from tensorflow.python.framework import composite_tensor as composite_tensor, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape, tensor_spec as tensor_spec, type_spec as type_spec
from tensorflow.python.ops import tensor_array_ops as tensor_array_ops
from tensorflow.python.ops.ragged import ragged_tensor as ragged_tensor
from tensorflow.python.util import deprecation as deprecation
from tensorflow.python.util.compat import collections_abc as collections_abc
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def normalize_element(element, element_signature: Any | None = ...): ...
def convert_legacy_structure(output_types, output_shapes, output_classes): ...
def from_compatible_tensor_list(element_spec, tensor_list): ...
def from_tensor_list(element_spec, tensor_list): ...
def get_flat_tensor_specs(element_spec): ...
def get_flat_tensor_shapes(element_spec): ...
def get_flat_tensor_types(element_spec): ...
def to_batched_tensor_list(element_spec, element): ...
def to_tensor_list(element_spec, element): ...
def are_compatible(spec1, spec2): ...
def type_spec_from_value(element, use_fallback: bool = ...): ...

class NoneTensor(composite_tensor.CompositeTensor): ...

class NoneTensorSpec(type_spec.BatchableTypeSpec):
    @property
    def value_type(self): ...
    @staticmethod
    def from_value(value): ...
    def most_specific_compatible_shape(self, other): ...
