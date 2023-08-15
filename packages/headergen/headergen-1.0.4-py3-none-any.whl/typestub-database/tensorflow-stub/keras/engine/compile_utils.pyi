from tensorflow.python.keras.utils import generic_utils as generic_utils, losses_utils as losses_utils, tf_utils as tf_utils
from tensorflow.python.ops import array_ops as array_ops, math_ops as math_ops
from tensorflow.python.util import nest as nest
from typing import Any

class Container:
    def __init__(self, output_names: Any | None = ...) -> None: ...
    def build(self, y_pred) -> None: ...

class LossesContainer(Container):
    def __init__(self, losses, loss_weights: Any | None = ..., output_names: Any | None = ...) -> None: ...
    @property
    def metrics(self): ...
    def build(self, y_pred) -> None: ...
    @property
    def built(self): ...
    def __call__(self, y_true, y_pred, sample_weight: Any | None = ..., regularization_losses: Any | None = ...): ...
    def reset_state(self) -> None: ...

class MetricsContainer(Container):
    def __init__(self, metrics: Any | None = ..., weighted_metrics: Any | None = ..., output_names: Any | None = ..., from_serialized: bool = ...) -> None: ...
    @property
    def metrics(self): ...
    @property
    def unweighted_metrics(self): ...
    @property
    def weighted_metrics(self): ...
    def build(self, y_pred, y_true) -> None: ...
    @property
    def built(self): ...
    def update_state(self, y_true, y_pred, sample_weight: Any | None = ...) -> None: ...
    def reset_state(self) -> None: ...

def create_pseudo_output_names(outputs): ...
def create_pseudo_input_names(inputs): ...
def map_to_output_names(y_pred, output_names, struct): ...
def map_missing_dict_keys(y_pred, struct): ...
def match_dtype_and_rank(y_t, y_p, sw): ...
def get_mask(y_p): ...
def apply_mask(y_p, sw, mask): ...
def get_custom_object_name(obj): ...
