from tensorflow.python.data.util import nest as nest
from tensorflow.python.framework import dtypes as dtypes, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape
from tensorflow.python.ops import sparse_ops as sparse_ops

def any_sparse(classes): ...
def as_dense_shapes(shapes, classes): ...
def as_dense_types(types, classes): ...
def deserialize_sparse_tensors(tensors, types, shapes, classes): ...
def get_classes(tensors): ...
def serialize_many_sparse_tensors(tensors): ...
def serialize_sparse_tensors(tensors): ...
