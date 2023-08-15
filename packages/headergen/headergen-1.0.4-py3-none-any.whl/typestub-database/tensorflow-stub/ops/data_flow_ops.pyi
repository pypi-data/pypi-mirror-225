from tensorflow.python.ops.gen_data_flow_ops import *
from tensorflow.python.eager import context as context
from tensorflow.python.framework import ops as ops, random_seed as random_seed, tensor_shape as tensor_shape, tensor_util as tensor_util
from tensorflow.python.lib.io import python_io as python_io
from tensorflow.python.ops import array_ops as array_ops, control_flow_ops as control_flow_ops, gen_data_flow_ops as gen_data_flow_ops, math_ops as math_ops, resource_variable_ops as resource_variable_ops
from tensorflow.python.util import deprecation as deprecation
from tensorflow.python.util.compat import collections_abc as collections_abc
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

class QueueBase:
    def __init__(self, dtypes, shapes, names, queue_ref) -> None: ...
    @staticmethod
    def from_list(index, queues): ...
    @property
    def queue_ref(self): ...
    @property
    def name(self): ...
    @property
    def dtypes(self): ...
    @property
    def shapes(self): ...
    @property
    def names(self): ...
    def enqueue(self, vals, name: Any | None = ...): ...
    def enqueue_many(self, vals, name: Any | None = ...): ...
    def dequeue(self, name: Any | None = ...): ...
    def dequeue_many(self, n, name: Any | None = ...): ...
    def dequeue_up_to(self, n, name: Any | None = ...): ...
    def close(self, cancel_pending_enqueues: bool = ..., name: Any | None = ...): ...
    def is_closed(self, name: Any | None = ...): ...
    def size(self, name: Any | None = ...): ...

class RandomShuffleQueue(QueueBase):
    def __init__(self, capacity, min_after_dequeue, dtypes, shapes: Any | None = ..., names: Any | None = ..., seed: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...

class FIFOQueue(QueueBase):
    def __init__(self, capacity, dtypes, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...

class GPUCompatibleFIFOQueue(QueueBase):
    def __init__(self, capacity, dtypes, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...
    def enqueue_many(self, vals, name: Any | None = ...) -> None: ...
    def dequeue_many(self, n, name: Any | None = ...) -> None: ...

class PaddingFIFOQueue(QueueBase):
    def __init__(self, capacity, dtypes, shapes, names: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...

class PriorityQueue(QueueBase):
    def __init__(self, capacity, types, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...

class Barrier:
    def __init__(self, types, shapes: Any | None = ..., shared_name: Any | None = ..., name: str = ...) -> None: ...
    @property
    def barrier_ref(self): ...
    @property
    def name(self): ...
    def insert_many(self, component_index, keys, values, name: Any | None = ...): ...
    def take_many(self, num_elements, allow_small_batch: bool = ..., timeout: Any | None = ..., name: Any | None = ...): ...
    def close(self, cancel_pending_enqueues: bool = ..., name: Any | None = ...): ...
    def ready_size(self, name: Any | None = ...): ...
    def incomplete_size(self, name: Any | None = ...): ...

class ConditionalAccumulatorBase:
    def __init__(self, dtype, shape, accumulator_ref) -> None: ...
    @property
    def accumulator_ref(self): ...
    @property
    def name(self): ...
    @property
    def dtype(self): ...
    def num_accumulated(self, name: Any | None = ...): ...
    def set_global_step(self, new_global_step, name: Any | None = ...): ...

class ConditionalAccumulator(ConditionalAccumulatorBase):
    def __init__(self, dtype, shape: Any | None = ..., shared_name: Any | None = ..., name: str = ..., reduction_type: str = ...) -> None: ...
    def apply_grad(self, grad, local_step: int = ..., name: Any | None = ...): ...
    def take_grad(self, num_required, name: Any | None = ...): ...

class SparseConditionalAccumulator(ConditionalAccumulatorBase):
    def __init__(self, dtype, shape: Any | None = ..., shared_name: Any | None = ..., name: str = ..., reduction_type: str = ...) -> None: ...
    def apply_indexed_slices_grad(self, grad, local_step: int = ..., name: Any | None = ...): ...
    def apply_grad(self, grad_indices, grad_values, grad_shape: Any | None = ..., local_step: int = ..., name: Any | None = ...): ...
    def take_grad(self, num_required, name: Any | None = ...): ...
    def take_indexed_slices_grad(self, num_required, name: Any | None = ...): ...
    def num_accumulated(self, name: Any | None = ...): ...
    def set_global_step(self, new_global_step, name: Any | None = ...): ...

class BaseStagingArea:
    def __init__(self, dtypes, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., capacity: int = ..., memory_limit: int = ...) -> None: ...
    @property
    def name(self): ...
    @property
    def dtypes(self): ...
    @property
    def shapes(self): ...
    @property
    def names(self): ...
    @property
    def capacity(self): ...
    @property
    def memory_limit(self): ...

class StagingArea(BaseStagingArea):
    def __init__(self, dtypes, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., capacity: int = ..., memory_limit: int = ...) -> None: ...
    def put(self, values, name: Any | None = ...): ...
    def get(self, name: Any | None = ...): ...
    def peek(self, index, name: Any | None = ...): ...
    def size(self, name: Any | None = ...): ...
    def clear(self, name: Any | None = ...): ...

class MapStagingArea(BaseStagingArea):
    def __init__(self, dtypes, shapes: Any | None = ..., names: Any | None = ..., shared_name: Any | None = ..., ordered: bool = ..., capacity: int = ..., memory_limit: int = ...) -> None: ...
    def put(self, key, vals, indices: Any | None = ..., name: Any | None = ...): ...
    def peek(self, key, indices: Any | None = ..., name: Any | None = ...): ...
    def get(self, key: Any | None = ..., indices: Any | None = ..., name: Any | None = ...): ...
    def size(self, name: Any | None = ...): ...
    def incomplete_size(self, name: Any | None = ...): ...
    def clear(self, name: Any | None = ...): ...

class RecordInput:
    def __init__(self, file_pattern, batch_size: int = ..., buffer_size: int = ..., parallelism: int = ..., shift_ratio: int = ..., seed: int = ..., name: Any | None = ..., batches: Any | None = ..., compression_type: Any | None = ...) -> None: ...
    def get_yield_op(self): ...
