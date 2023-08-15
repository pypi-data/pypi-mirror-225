from tensorflow.python.framework import ops as ops
from tensorflow.python.ops import array_ops as array_ops, gen_boosted_trees_ops as gen_boosted_trees_ops, resources as resources
from tensorflow.python.ops.gen_boosted_trees_ops import boosted_trees_aggregate_stats as boosted_trees_aggregate_stats, boosted_trees_bucketize as boosted_trees_bucketize, boosted_trees_sparse_aggregate_stats as boosted_trees_sparse_aggregate_stats
from tensorflow.python.training import saver as saver
from tensorflow.python.training.tracking import tracking as tracking
from typing import Any

class PruningMode:
    NO_PRUNING: Any
    PRE_PRUNING: Any
    POST_PRUNING: Any
    @classmethod
    def from_str(cls, mode): ...

class QuantileAccumulatorSaveable(saver.BaseSaverBuilder.SaveableObject):
    def __init__(self, resource_handle, create_op, num_streams, name): ...
    def restore(self, restored_tensors, unused_tensor_shapes): ...

class QuantileAccumulator(tracking.TrackableResource):
    def __init__(self, epsilon, num_streams, num_quantiles, name: Any | None = ..., max_elements: Any | None = ...) -> None: ...
    @property
    def initializer(self): ...
    def is_initialized(self): ...
    @property
    def saveable(self): ...
    def add_summaries(self, float_columns, example_weights): ...
    def flush(self): ...
    def get_bucket_boundaries(self): ...

class _TreeEnsembleSavable(saver.BaseSaverBuilder.SaveableObject):
    def __init__(self, resource_handle, create_op, name) -> None: ...
    def restore(self, restored_tensors, unused_restored_shapes): ...

class TreeEnsemble(tracking.TrackableResource):
    def __init__(self, name, stamp_token: int = ..., is_local: bool = ..., serialized_proto: str = ...) -> None: ...
    @property
    def initializer(self): ...
    def is_initialized(self): ...
    def get_stamp_token(self): ...
    def get_states(self): ...
    def serialize(self): ...
    def deserialize(self, stamp_token, serialized_proto): ...
