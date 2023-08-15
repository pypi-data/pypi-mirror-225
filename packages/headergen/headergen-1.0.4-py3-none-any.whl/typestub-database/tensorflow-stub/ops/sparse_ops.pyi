from tensorflow.python.ops.gen_sparse_ops import *
from tensorflow.python.framework import constant_op as constant_op, dtypes as dtypes, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape, tensor_util as tensor_util
from tensorflow.python.ops import array_ops as array_ops, check_ops as check_ops, control_flow_ops as control_flow_ops, gen_sparse_ops as gen_sparse_ops, math_ops as math_ops, special_math_ops as special_math_ops
from tensorflow.python.util import compat as compat, deprecation as deprecation, dispatch as dispatch, nest as nest, tf_inspect as tf_inspect
from tensorflow.python.util.compat import collections_abc as collections_abc
from tensorflow.python.util.tf_export import get_canonical_name_for_symbol as get_canonical_name_for_symbol, tf_export as tf_export
from typing import Any

def from_dense(tensor, name: Any | None = ...): ...
def sparse_expand_dims(sp_input, axis: Any | None = ..., name: Any | None = ...): ...
def sparse_eye(num_rows, num_columns: Any | None = ..., dtype=..., name: Any | None = ...): ...
def sparse_concat(axis, sp_inputs, name: Any | None = ..., expand_nonconcat_dim: bool = ..., concat_dim: Any | None = ..., expand_nonconcat_dims: Any | None = ...): ...
def sparse_concat_v2(axis, sp_inputs, expand_nonconcat_dims: bool = ..., name: Any | None = ...): ...
def sparse_add(a, b, threshold: Any | None = ..., thresh: Any | None = ...): ...
def sparse_add_v2(a, b, threshold: int = ...): ...
def sparse_cross(inputs, name: Any | None = ..., separator: Any | None = ...): ...
def sparse_cross_hashed(inputs, num_buckets: int = ..., hash_key: Any | None = ..., name: Any | None = ...): ...
def sparse_dense_cwise_add(sp_t, dense_t): ...
def sparse_reorder(sp_input, name: Any | None = ...): ...
def sparse_reshape(sp_input, shape, name: Any | None = ...): ...

class KeywordRequired: ...

def sparse_split(keyword_required=..., sp_input: Any | None = ..., num_split: Any | None = ..., axis: Any | None = ..., name: Any | None = ..., split_dim: Any | None = ...): ...
def sparse_split_v2(sp_input: Any | None = ..., num_split: Any | None = ..., axis: Any | None = ..., name: Any | None = ...): ...
def sparse_slice(sp_input, start, size, name: Any | None = ...): ...
def sparse_to_dense(sparse_indices, output_shape, sparse_values, default_value: int = ..., validate_indices: bool = ..., name: Any | None = ...): ...
def sparse_reduce_max_v2(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., output_is_sparse: bool = ..., name: Any | None = ...): ...
def sparse_reduce_max(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., reduction_axes: Any | None = ..., keep_dims: Any | None = ...): ...
def sparse_reduce_max_sparse(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., reduction_axes: Any | None = ..., keep_dims: Any | None = ...): ...
def sparse_reduce_sum_v2(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., output_is_sparse: bool = ..., name: Any | None = ...): ...
def sparse_reduce_sum(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., reduction_axes: Any | None = ..., keep_dims: Any | None = ...): ...
def sparse_reduce_sum_sparse(sp_input, axis: Any | None = ..., keepdims: Any | None = ..., reduction_axes: Any | None = ..., keep_dims: Any | None = ...): ...
def sparse_tensor_to_dense(sp_input, default_value: Any | None = ..., validate_indices: bool = ..., name: Any | None = ...): ...
def sparse_to_indicator(sp_input, vocab_size, name: Any | None = ...): ...
def sparse_merge(sp_ids, sp_values, vocab_size, name: Any | None = ..., already_sorted: bool = ...): ...
def sparse_merge_impl(sp_ids, sp_values, vocab_size, name: Any | None = ..., already_sorted: bool = ...): ...
def sparse_retain(sp_input, to_retain): ...
def sparse_reset_shape(sp_input, new_shape: Any | None = ...): ...
def sparse_fill_empty_rows(sp_input, default_value, name: Any | None = ...): ...
def serialize_sparse(sp_input, name: Any | None = ..., out_type=...): ...
def serialize_sparse_v2(sp_input, out_type=..., name: Any | None = ...): ...
def serialize_many_sparse(sp_input, name: Any | None = ..., out_type=...): ...
def serialize_many_sparse_v2(sp_input, out_type=..., name: Any | None = ...): ...
def deserialize_sparse(serialized_sparse, dtype, rank: Any | None = ..., name: Any | None = ...): ...
def deserialize_many_sparse(serialized_sparse, dtype, rank: Any | None = ..., name: Any | None = ...): ...
def sparse_tensor_dense_matmul(sp_a, b, adjoint_a: bool = ..., adjoint_b: bool = ..., name: Any | None = ...): ...
def sparse_softmax(sp_input, name: Any | None = ...): ...
def sparse_maximum(sp_a, sp_b, name: Any | None = ...): ...
def sparse_minimum(sp_a, sp_b, name: Any | None = ...): ...
def sparse_transpose(sp_input, perm: Any | None = ..., name: Any | None = ...): ...
def map_values(op, *args, **kwargs): ...

class _UnaryMapValueDispatcher(dispatch.OpDispatcher):
    def __init__(self, original_func) -> None: ...
    def handle(self, args, kwargs): ...
