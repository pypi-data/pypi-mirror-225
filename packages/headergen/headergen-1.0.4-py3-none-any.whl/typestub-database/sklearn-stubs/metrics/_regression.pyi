from .._loss.glm_distribution import TweedieDistribution as TweedieDistribution
from ..exceptions import UndefinedMetricWarning as UndefinedMetricWarning
from ..utils.validation import check_array as check_array, check_consistent_length as check_consistent_length, column_or_1d as column_or_1d
from typing import Any

__ALL__: Any

def mean_absolute_error(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ...): ...
def mean_pinball_loss(y_true, y_pred, *, sample_weight: Any | None = ..., alpha: float = ..., multioutput: str = ...): ...
def mean_absolute_percentage_error(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ...): ...
def mean_squared_error(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ..., squared: bool = ...): ...
def mean_squared_log_error(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ..., squared: bool = ...): ...
def median_absolute_error(y_true, y_pred, *, multioutput: str = ..., sample_weight: Any | None = ...): ...
def explained_variance_score(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ...): ...
def r2_score(y_true, y_pred, *, sample_weight: Any | None = ..., multioutput: str = ...): ...
def max_error(y_true, y_pred): ...
def mean_tweedie_deviance(y_true, y_pred, *, sample_weight: Any | None = ..., power: int = ...): ...
def mean_poisson_deviance(y_true, y_pred, *, sample_weight: Any | None = ...): ...
def mean_gamma_deviance(y_true, y_pred, *, sample_weight: Any | None = ...): ...
def d2_tweedie_score(y_true, y_pred, *, sample_weight: Any | None = ..., power: int = ...): ...
