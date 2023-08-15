from keras.optimizer_experimental import optimizer as optimizer
from keras.utils import generic_utils as generic_utils
from typing import Any

class RMSprop(optimizer.Optimizer):
    rho: Any
    momentum: Any
    epsilon: Any
    centered: Any
    def __init__(self, learning_rate: float = ..., rho: float = ..., momentum: float = ..., epsilon: float = ..., centered: bool = ..., clipnorm: Any | None = ..., clipvalue: Any | None = ..., global_clipnorm: Any | None = ..., use_ema: bool = ..., ema_momentum: float = ..., ema_overwrite_frequency: int = ..., jit_compile: bool = ..., name: str = ..., **kwargs) -> None: ...
    def build(self, var_list) -> None: ...
    def update_step(self, gradient, variable, params: Any | None = ...) -> None: ...
    def get_config(self): ...
