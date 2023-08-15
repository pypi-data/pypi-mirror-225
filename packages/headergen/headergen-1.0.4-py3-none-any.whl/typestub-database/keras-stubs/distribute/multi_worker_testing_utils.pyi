from keras.optimizer_v2 import gradient_descent as gradient_descent
from typing import Any

ASSIGNED_PORTS: Any
lock: Any

def mnist_synthetic_dataset(batch_size, steps_per_epoch): ...
def get_mnist_model(input_shape): ...
def make_parameter_server_cluster(num_workers, num_ps): ...
def pick_unused_port(): ...
def create_in_process_cluster(num_workers, num_ps, has_chief: bool = ..., has_eval: bool = ..., rpc_layer: str = ...): ...
