from tensorflow.python.eager import context as context
from tensorflow.python.framework import errors as errors
from tensorflow.python.util import deprecation as deprecation
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any, Union

def tensor_float_32_execution_enabled(): ...
def enable_tensor_float_32_execution(enabled) -> None: ...
def get_intra_op_parallelism_threads(): ...
def set_intra_op_parallelism_threads(num_threads) -> None: ...
def get_inter_op_parallelism_threads(): ...
def set_inter_op_parallelism_threads(num_threads) -> None: ...
def get_optimizer_jit() -> str: ...
def set_optimizer_jit(enabled: Union[bool, str]): ...
def get_optimizer_experimental_options(): ...
def set_optimizer_experimental_options(options) -> None: ...
def get_soft_device_placement(): ...
def set_soft_device_placement(enabled) -> None: ...
def get_device_policy(): ...
def set_device_policy(device_policy) -> None: ...
def get_synchronous_execution(): ...
def set_synchronous_execution(enable) -> None: ...
def list_physical_devices(device_type: Any | None = ...): ...
def list_logical_devices(device_type: Any | None = ...): ...
def get_visible_devices(device_type: Any | None = ...): ...
def set_visible_devices(devices, device_type: Any | None = ...) -> None: ...
def get_memory_info(device): ...
def reset_memory_stats(device) -> None: ...
def get_memory_usage(device): ...
def get_memory_growth(device): ...
def set_memory_growth(device, enable) -> None: ...
def get_device_details(device): ...
def get_logical_device_configuration(device): ...
def set_logical_device_configuration(device, logical_devices) -> None: ...
def enable_mlir_bridge() -> None: ...
def enable_mlir_graph_optimization() -> None: ...
def disable_mlir_bridge() -> None: ...
def disable_mlir_graph_optimization() -> None: ...
def enable_op_determinism() -> None: ...
def disable_op_determinism() -> None: ...
def is_op_determinism_enabled(): ...
