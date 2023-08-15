from tensorflow.python.framework import dtypes as dtypes, indexed_slices as indexed_slices, tensor_util as tensor_util
from tensorflow.python.ops import array_ops as array_ops, control_flow_ops as control_flow_ops, math_ops as math_ops
from tensorflow.python.ops.numpy_ops import np_arrays as np_arrays, np_dtypes as np_dtypes, np_export as np_export
from tensorflow.python.types import core as core
from tensorflow.python.util import nest as nest
from typing import Any

def isscalar(val): ...
def get_np_doc_form(): ...
def set_np_doc_form(value) -> None: ...

class Link:
    value: Any
    def __init__(self, v) -> None: ...

class AliasOf:
    value: Any
    def __init__(self, v) -> None: ...

class NoLink: ...

def generate_link(flag, np_fun_name): ...
def is_check_link(): ...
def set_check_link(value) -> None: ...
def is_sig_mismatch_an_error(): ...
def set_is_sig_mismatch_an_error(value) -> None: ...
def np_doc(np_fun_name, np_fun: Any | None = ..., export: bool = ..., unsupported_params: Any | None = ..., link: Any | None = ...): ...
def np_doc_only(np_fun_name, np_fun: Any | None = ..., export: bool = ...): ...
def finfo(dtype): ...
def result_type(*arrays_and_dtypes): ...
def result_type_unary(a, dtype): ...
def promote_types(type1, type2): ...
def tf_broadcast(*args): ...
def get_static_value(x): ...
def cond(pred, true_fn, false_fn): ...
def add(a, b): ...
def subtract(a, b): ...
def greater(a, b): ...
def greater_equal(a, b): ...
def less_equal(a, b): ...
def logical_and(a, b): ...
def logical_or(a, b): ...
def getitem(a, slice_spec): ...
def reduce_all(input_tensor, axis: Any | None = ..., keepdims: bool = ...): ...
def reduce_any(input_tensor, axis: Any | None = ..., keepdims: bool = ...): ...
def tf_rank(t): ...
