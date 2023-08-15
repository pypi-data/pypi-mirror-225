from tensorflow.python.eager import context as context
from tensorflow.python.framework import dtypes as dtypes, ops as ops
from tensorflow.python.ops import array_ops as array_ops, confusion_matrix as confusion_matrix, control_flow_ops as control_flow_ops, math_ops as math_ops, nn as nn, nn_ops as nn_ops, weights_broadcast_ops as weights_broadcast_ops
from tensorflow.python.ops.losses import util as util
from tensorflow.python.util import dispatch as dispatch
from tensorflow.python.util.deprecation import deprecated_args as deprecated_args, deprecated_argument_lookup as deprecated_argument_lookup
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

class Reduction:
    NONE: str
    SUM: str
    SUM_OVER_BATCH_SIZE: str
    MEAN: str
    SUM_BY_NONZERO_WEIGHTS: str
    SUM_OVER_NONZERO_WEIGHTS: Any
    @classmethod
    def all(cls): ...
    @classmethod
    def validate(cls, key) -> None: ...

def compute_weighted_loss(losses, weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def absolute_difference(labels, predictions, weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def cosine_distance(labels, predictions, axis: Any | None = ..., weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=..., dim: Any | None = ...): ...
def hinge_loss(labels, logits, weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def huber_loss(labels, predictions, weights: float = ..., delta: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def log_loss(labels, predictions, weights: float = ..., epsilon: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def mean_pairwise_squared_error(labels, predictions, weights: float = ..., scope: Any | None = ..., loss_collection=...): ...
def mean_squared_error(labels, predictions, weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def sigmoid_cross_entropy(multi_class_labels, logits, weights: float = ..., label_smoothing: int = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def softmax_cross_entropy(onehot_labels, logits, weights: float = ..., label_smoothing: int = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
def sparse_softmax_cross_entropy(labels, logits, weights: float = ..., scope: Any | None = ..., loss_collection=..., reduction=...): ...
