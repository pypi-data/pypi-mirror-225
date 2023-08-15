from tensorflow.python import tf2 as tf2
from tensorflow.python.eager import context as context
from tensorflow.python.framework import config as config, dtypes as dtypes, ops as ops, tensor_shape as tensor_shape, tensor_spec as tensor_spec, test_util as test_util
from tensorflow.python.keras import backend as backend, layers as layers, models as models
from tensorflow.python.keras.engine import base_layer_utils as base_layer_utils
from tensorflow.python.keras.utils import tf_contextlib as tf_contextlib, tf_inspect as tf_inspect
from tensorflow.python.util import tf_decorator as tf_decorator
from typing import Any

def string_test(actual, expected) -> None: ...
def numeric_test(actual, expected) -> None: ...
def get_test_data(train_samples, test_samples, input_shape, num_classes, random_seed: Any | None = ...): ...
def layer_test(layer_cls, kwargs: Any | None = ..., input_shape: Any | None = ..., input_dtype: Any | None = ..., input_data: Any | None = ..., expected_output: Any | None = ..., expected_output_dtype: Any | None = ..., expected_output_shape: Any | None = ..., validate_training: bool = ..., adapt_data: Any | None = ..., custom_objects: Any | None = ..., test_harness: Any | None = ..., supports_masking: Any | None = ...): ...
def model_type_scope(value) -> None: ...
def run_eagerly_scope(value) -> None: ...
def should_run_eagerly(): ...
def saved_model_format_scope(value, **kwargs) -> None: ...
def get_save_format(): ...
def get_save_kwargs(): ...
def get_model_type(): ...
def get_small_sequential_mlp(num_hidden, num_classes, input_dim: Any | None = ...): ...
def get_small_functional_mlp(num_hidden, num_classes, input_dim): ...

class SmallSubclassMLP(models.Model):
    use_bn: Any
    use_dp: Any
    layer_a: Any
    layer_b: Any
    dp: Any
    bn: Any
    def __init__(self, num_hidden, num_classes, use_bn: bool = ..., use_dp: bool = ..., **kwargs) -> None: ...
    def call(self, inputs, **kwargs): ...

class _SmallSubclassMLPCustomBuild(models.Model):
    layer_a: Any
    layer_b: Any
    num_hidden: Any
    num_classes: Any
    def __init__(self, num_hidden, num_classes) -> None: ...
    def build(self, input_shape) -> None: ...
    def call(self, inputs, **kwargs): ...

def get_small_subclass_mlp(num_hidden, num_classes): ...
def get_small_subclass_mlp_with_custom_build(num_hidden, num_classes): ...
def get_small_mlp(num_hidden, num_classes, input_dim): ...

class _SubclassModel(models.Model):
    num_layers: Any
    def __init__(self, model_layers, *args, **kwargs) -> None: ...
    def call(self, inputs, **kwargs): ...

class _SubclassModelCustomBuild(models.Model):
    all_layers: Any
    def __init__(self, layer_generating_func, *args, **kwargs) -> None: ...
    def build(self, input_shape) -> None: ...
    def call(self, inputs, **kwargs): ...

def get_model_from_layers(model_layers, input_shape: Any | None = ..., input_dtype: Any | None = ..., name: Any | None = ..., input_ragged: Any | None = ..., input_sparse: Any | None = ..., model_type: Any | None = ...): ...

class Bias(layers.Layer):
    bias: Any
    def build(self, input_shape) -> None: ...
    def call(self, inputs): ...

class _MultiIOSubclassModel(models.Model):
    def __init__(self, branch_a, branch_b, shared_input_branch: Any | None = ..., shared_output_branch: Any | None = ..., name: Any | None = ...) -> None: ...
    def call(self, inputs, **kwargs): ...

class _MultiIOSubclassModelCustomBuild(models.Model):
    def __init__(self, branch_a_func, branch_b_func, shared_input_branch_func: Any | None = ..., shared_output_branch_func: Any | None = ...) -> None: ...
    def build(self, input_shape) -> None: ...
    def call(self, inputs, **kwargs): ...

def get_multi_io_model(branch_a, branch_b, shared_input_branch: Any | None = ..., shared_output_branch: Any | None = ...): ...
def get_v2_optimizer(name, **kwargs): ...
def get_expected_metric_variable_names(var_names, name_suffix: str = ...): ...
def enable_v2_dtype_behavior(fn): ...
def disable_v2_dtype_behavior(fn): ...
def device(should_use_gpu) -> None: ...
def use_gpu() -> None: ...
def for_all_test_methods(decorator, *args, **kwargs): ...
def run_without_tensor_float_32(description): ...
def run_all_without_tensor_float_32(description): ...
def run_v2_only(func: Any | None = ...): ...
def generate_combinations_with_testcase_name(**kwargs): ...
