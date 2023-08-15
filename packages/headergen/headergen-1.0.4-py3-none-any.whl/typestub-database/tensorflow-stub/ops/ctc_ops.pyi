from tensorflow.python.eager import context as context
from tensorflow.python.framework import constant_op as constant_op, device as device, dtypes as dtypes, function as function, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape
from tensorflow.python.ops import array_ops as array_ops, custom_gradient as custom_gradient, functional_ops as functional_ops, gen_ctc_ops as gen_ctc_ops, inplace_ops as inplace_ops, linalg_ops as linalg_ops, map_fn as map_fn, math_ops as math_ops, nn_ops as nn_ops, sparse_ops as sparse_ops
from tensorflow.python.util import deprecation as deprecation, dispatch as dispatch, nest as nest
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def ctc_loss(labels, inputs: Any | None = ..., sequence_length: Any | None = ..., preprocess_collapse_repeated: bool = ..., ctc_merge_repeated: bool = ..., ignore_longer_outputs_than_inputs: bool = ..., time_major: bool = ..., logits: Any | None = ...): ...
def ctc_greedy_decoder(inputs, sequence_length, merge_repeated: bool = ..., blank_index: Any | None = ...): ...
def ctc_beam_search_decoder(inputs, sequence_length, beam_width: int = ..., top_paths: int = ..., merge_repeated: bool = ...): ...
def ctc_beam_search_decoder_v2(inputs, sequence_length, beam_width: int = ..., top_paths: int = ...): ...
def ctc_state_log_probs(seq_lengths, max_seq_length): ...
def ctc_loss_and_grad(logits, labels, label_length, logit_length, unique: Any | None = ...): ...
def ctc_loss_v2(labels, logits, label_length, logit_length, logits_time_major: bool = ..., unique: Any | None = ..., blank_index: Any | None = ..., name: Any | None = ...): ...
def ctc_loss_v3(labels, logits, label_length, logit_length, logits_time_major: bool = ..., unique: Any | None = ..., blank_index: Any | None = ..., name: Any | None = ...): ...
def ctc_loss_dense(labels, logits, label_length, logit_length, logits_time_major: bool = ..., unique: Any | None = ..., blank_index: int = ..., name: Any | None = ...): ...
def collapse_repeated(labels, seq_length, name: Any | None = ...): ...
def dense_labels_to_sparse(dense, length): ...
def ctc_unique_labels(labels, name: Any | None = ...): ...
