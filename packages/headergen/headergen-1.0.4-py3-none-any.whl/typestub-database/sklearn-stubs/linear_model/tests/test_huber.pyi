from sklearn.datasets import make_regression as make_regression
from sklearn.linear_model import HuberRegressor as HuberRegressor, LinearRegression as LinearRegression, Ridge as Ridge, SGDRegressor as SGDRegressor
from sklearn.utils._testing import assert_almost_equal as assert_almost_equal, assert_array_almost_equal as assert_array_almost_equal, assert_array_equal as assert_array_equal

def make_regression_with_outliers(n_samples: int = ..., n_features: int = ...): ...
def test_huber_equals_lr_for_high_epsilon() -> None: ...
def test_huber_max_iter() -> None: ...
def test_huber_gradient(): ...
def test_huber_sample_weights() -> None: ...
def test_huber_sparse() -> None: ...
def test_huber_scaling_invariant() -> None: ...
def test_huber_and_sgd_same_results() -> None: ...
def test_huber_warm_start() -> None: ...
def test_huber_better_r2_score() -> None: ...
def test_huber_bool() -> None: ...
