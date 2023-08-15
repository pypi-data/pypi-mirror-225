from statsmodels.tools.numdiff import approx_fprime_cs as approx_fprime_cs
from statsmodels.tsa import arima_process as arima_process
from statsmodels.tsa.statespace.tools import prefix_dtype_map as prefix_dtype_map
from typing import Any

NON_STATIONARY_ERROR: str

def arma_innovations(endog, ar_params: Any | None = ..., ma_params: Any | None = ..., sigma2: int = ..., normalize: bool = ..., prefix: Any | None = ...): ...
def arma_loglike(endog, ar_params: Any | None = ..., ma_params: Any | None = ..., sigma2: int = ..., prefix: Any | None = ...): ...
def arma_loglikeobs(endog, ar_params: Any | None = ..., ma_params: Any | None = ..., sigma2: int = ..., prefix: Any | None = ...): ...
def arma_score(endog, ar_params: Any | None = ..., ma_params: Any | None = ..., sigma2: int = ..., prefix: Any | None = ...): ...
def arma_scoreobs(endog, ar_params: Any | None = ..., ma_params: Any | None = ..., sigma2: int = ..., prefix: Any | None = ...): ...
