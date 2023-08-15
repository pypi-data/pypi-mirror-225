from tensorflow.python.framework.test_util import assert_equal_graph_def as assert_equal_graph_def, create_local_cluster as create_local_cluster, gpu_device_name as gpu_device_name, is_gpu_available as is_gpu_available
from tensorflow.python.ops.gradient_checker import compute_gradient as compute_gradient, compute_gradient_error as compute_gradient_error
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

Benchmark: Any
StubOutForTesting: Any

def main(argv: Any | None = ...): ...
def get_temp_dir(): ...
def test_src_dir_path(relative_path): ...
def is_built_with_cuda(): ...
def is_built_with_rocm(): ...
def disable_with_predicate(pred, skip_message): ...
def is_built_with_gpu_support(): ...
def is_built_with_xla(): ...
