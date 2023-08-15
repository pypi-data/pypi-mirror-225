from tensorflow.python.distribute import distribution_strategy_context as distribution_strategy_context
from tensorflow.python.eager import context as context
from tensorflow.python.framework import dtypes as dtypes, ops as ops, sparse_tensor as sparse_tensor
from tensorflow.python.ops import array_ops as array_ops, check_ops as check_ops, confusion_matrix as confusion_matrix, control_flow_ops as control_flow_ops, math_ops as math_ops, nn as nn, sets as sets, sparse_ops as sparse_ops, state_ops as state_ops, variable_scope as variable_scope, weights_broadcast_ops as weights_broadcast_ops
from tensorflow.python.util.deprecation import deprecated as deprecated
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def metric_variable(shape, dtype, validate_shape: bool = ..., name: Any | None = ...): ...
def mean(values, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def accuracy(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def auc(labels, predictions, weights: Any | None = ..., num_thresholds: int = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., curve: str = ..., name: Any | None = ..., summation_method: str = ..., thresholds: Any | None = ...): ...
def mean_absolute_error(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_cosine_distance(labels, predictions, dim, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_per_class_accuracy(labels, predictions, num_classes, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_iou(labels, predictions, num_classes, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_relative_error(labels, predictions, normalizer, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_squared_error(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def mean_tensor(values, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def percentage_below(values, threshold, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def false_negatives(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def false_negatives_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def false_positives(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def false_positives_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def true_negatives(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def true_negatives_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def true_positives(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def true_positives_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def precision(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def precision_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def recall(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def recall_at_k(labels, predictions, k, class_id: Any | None = ..., weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def recall_at_top_k(labels, predictions_idx, k: Any | None = ..., class_id: Any | None = ..., weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def recall_at_thresholds(labels, predictions, thresholds, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def root_mean_squared_error(labels, predictions, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def sensitivity_at_specificity(labels, predictions, specificity, weights: Any | None = ..., num_thresholds: int = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def sparse_average_precision_at_k(labels, predictions, k, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def average_precision_at_k(labels, predictions, k, weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def precision_at_top_k(labels, predictions_idx, k: Any | None = ..., class_id: Any | None = ..., weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def sparse_precision_at_k(labels, predictions, k, class_id: Any | None = ..., weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def precision_at_k(labels, predictions, k, class_id: Any | None = ..., weights: Any | None = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
def specificity_at_sensitivity(labels, predictions, sensitivity, weights: Any | None = ..., num_thresholds: int = ..., metrics_collections: Any | None = ..., updates_collections: Any | None = ..., name: Any | None = ...): ...
