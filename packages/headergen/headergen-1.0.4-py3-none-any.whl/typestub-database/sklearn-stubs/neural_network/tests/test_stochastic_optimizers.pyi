from sklearn.neural_network._stochastic_optimizers import AdamOptimizer as AdamOptimizer, BaseOptimizer as BaseOptimizer, SGDOptimizer as SGDOptimizer
from sklearn.utils._testing import assert_array_equal as assert_array_equal
from typing import Any

shapes: Any

def test_base_optimizer() -> None: ...
def test_sgd_optimizer_no_momentum() -> None: ...
def test_sgd_optimizer_momentum() -> None: ...
def test_sgd_optimizer_trigger_stopping() -> None: ...
def test_sgd_optimizer_nesterovs_momentum() -> None: ...
def test_adam_optimizer() -> None: ...
