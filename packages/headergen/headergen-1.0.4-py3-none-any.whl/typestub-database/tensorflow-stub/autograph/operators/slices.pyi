from tensorflow.python.framework import dtypes as dtypes, tensor_util as tensor_util
from tensorflow.python.ops import gen_array_ops as gen_array_ops, gen_string_ops as gen_string_ops, list_ops as list_ops, tensor_array_ops as tensor_array_ops

class GetItemOpts: ...

def get_item(target, i, opts): ...
def set_item(target, i, x): ...
