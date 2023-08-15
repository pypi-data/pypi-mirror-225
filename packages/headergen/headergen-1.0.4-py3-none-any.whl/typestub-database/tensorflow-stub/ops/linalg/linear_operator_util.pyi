from tensorflow.python.framework import dtypes as dtypes, ops as ops
from tensorflow.python.module import module as module
from tensorflow.python.ops import array_ops as array_ops, check_ops as check_ops, control_flow_ops as control_flow_ops, linalg_ops as linalg_ops, math_ops as math_ops
from tensorflow.python.util import nest as nest
from typing import Any

def convert_nonref_to_tensor(value, dtype: Any | None = ..., dtype_hint: Any | None = ..., name: Any | None = ...): ...
def base_dtype(dtype): ...
def dtype_name(dtype): ...
def check_dtype(arg, dtype) -> None: ...
def is_ref(x): ...
def assert_not_ref_type(x, arg_name) -> None: ...
def assert_no_entries_with_modulus_zero(x, message: Any | None = ..., name: str = ...): ...
def assert_zero_imag_part(x, message: Any | None = ..., name: str = ...): ...
def assert_compatible_matrix_dimensions(operator, x): ...
def assert_is_batch_matrix(tensor) -> None: ...
def shape_tensor(shape, name: Any | None = ...): ...
def broadcast_matrix_batch_dims(batch_matrices, name: Any | None = ...): ...
def matrix_solve_with_broadcast(matrix, rhs, adjoint: bool = ..., name: Any | None = ...): ...
def use_operator_or_provided_hint_unless_contradicting(operator, hint_attr_name, provided_hint_value, message): ...
def arg_is_blockwise(block_dimensions, arg, arg_split_dim): ...
def split_arg_into_blocks(block_dims, block_dims_fn, arg, axis: int = ...): ...
