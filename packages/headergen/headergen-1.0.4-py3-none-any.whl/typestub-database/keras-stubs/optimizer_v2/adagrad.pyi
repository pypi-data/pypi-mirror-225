from keras import backend_config as backend_config
from keras.optimizer_v2 import optimizer_v2 as optimizer_v2
from typing import Any

class Adagrad(optimizer_v2.OptimizerV2):
    epsilon: Any
    def __init__(self, learning_rate: float = ..., initial_accumulator_value: float = ..., epsilon: float = ..., name: str = ..., **kwargs) -> None: ...
    def set_weights(self, weights) -> None: ...
    @classmethod
    def from_config(cls, config, custom_objects: Any | None = ...): ...
    def get_config(self): ...
