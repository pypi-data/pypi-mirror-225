from tensorflow.python.framework import tensor_util as tensor_util
from tensorflow.python.keras import backend as backend
from tensorflow.python.ops import array_ops as array_ops
from tensorflow.python.util import nest as nest
from typing import Any

class PartialBatchPaddingHandler:
    padded_batch_size: int
    padding_mask: Any
    output_shape: Any
    def __init__(self, output_shape) -> None: ...
    def get_real_batch_size(self, dataset_batch): ...
    def update_mask(self, padding_mask, dataset_batch): ...
    def pad_batch(self, *dataset_batch_elements): ...
    def apply_mask(self, prediction_result): ...
