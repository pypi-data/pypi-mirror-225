from tensorflow.python.framework import dtypes as dtypes, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape, tensor_spec as tensor_spec
from tensorflow.python.keras.engine import base_layer as base_layer
from tensorflow.python.keras.utils import tf_utils as tf_utils
from tensorflow.python.ops import array_ops as array_ops, sparse_ops as sparse_ops
from tensorflow.python.ops.ragged import ragged_array_ops as ragged_array_ops, ragged_tensor as ragged_tensor
from tensorflow.python.util.tf_export import keras_export as keras_export
from typing import Any

class CategoryCrossing(base_layer.Layer):
    depth: Any
    separator: Any
    def __init__(self, depth: Any | None = ..., name: Any | None = ..., separator: str = ..., **kwargs) -> None: ...
    def partial_crossing(self, partial_inputs, ragged_out, sparse_out): ...
    def call(self, inputs): ...
    def compute_output_shape(self, input_shape): ...
    def compute_output_signature(self, input_spec): ...
    def get_config(self): ...
