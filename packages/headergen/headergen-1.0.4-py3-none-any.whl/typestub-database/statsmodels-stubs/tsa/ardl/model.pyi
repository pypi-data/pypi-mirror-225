import datetime as dt
import matplotlib.figure
import numpy as np
import pandas as pd
import statsmodels.base.wrapper as wrap
from statsmodels.compat.python import Literal
from statsmodels.iolib.summary import Summary
from statsmodels.tsa.ar_model import AROrderSelectionResults, AutoReg, AutoRegResults
from statsmodels.tsa.deterministic import DeterministicProcess
from typing import Any, Dict, Hashable, List, NamedTuple, Optional, Sequence, Tuple, Union

class BoundsTestResult(NamedTuple):
    stat: float
    crit_vals: pd.DataFrame
    p_values: pd.Series
    null: str
    alternative: str

class ARDL(AutoReg):
    def __init__(self, endog: Union[Sequence[float], pd.Series, _ArrayLike2D], lags: Union[None, int, Sequence[int]], exog: Optional[_ArrayLike2D] = ..., order: _ARDLOrder = ..., trend: Any = ..., *, fixed: Optional[_ArrayLike2D] = ..., causal: bool = ..., seasonal: bool = ..., deterministic: Optional[DeterministicProcess] = ..., hold_back: Optional[int] = ..., period: Optional[int] = ..., missing: Any = ...) -> None: ...
    @property
    def fixed(self) -> Union[None, np.ndarray, pd.DataFrame]: ...
    @property
    def causal(self) -> bool: ...
    @property
    def ar_lags(self) -> Optional[List[int]]: ...
    @property
    def dl_lags(self) -> Dict[Hashable, List[int]]: ...
    @property
    def ardl_order(self) -> Tuple[int, ...]: ...
    def fit(self, *, cov_type: str = ..., cov_kwds: Dict[str, Any] = ..., use_t: bool = ...) -> ARDLResults: ...
    def predict(self, params: _ArrayLike1D, start: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., end: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., dynamic: bool = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., exog_oos: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ..., fixed_oos: Union[None, np.ndarray, pd.DataFrame] = ...): ...
    @classmethod
    def from_formula(cls, formula: str, data: pd.DataFrame, lags: Union[None, int, Sequence[int]] = ..., order: _ARDLOrder = ..., trend: Any = ..., *, causal: bool = ..., seasonal: bool = ..., deterministic: Optional[DeterministicProcess] = ..., hold_back: Optional[int] = ..., period: Optional[int] = ..., missing: Any = ...) -> ARDL: ...

class ARDLResults(AutoRegResults):
    cov_params_default: Any
    def __init__(self, model: ARDL, params: np.ndarray, cov_params: np.ndarray, normalized_cov_params: Optional[np.ndarray] = ..., scale: float = ..., use_t: bool = ...) -> None: ...
    def predict(self, start: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., end: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., dynamic: bool = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., exog_oos: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ..., fixed_oos: Union[None, np.ndarray, pd.DataFrame] = ...): ...
    def forecast(self, steps: int = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ...) -> Union[np.ndarray, pd.Series]: ...
    def get_prediction(self, start: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., end: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., dynamic: bool = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., exog_oos: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ..., fixed_oos: Union[None, np.ndarray, pd.DataFrame] = ...) -> Union[np.ndarray, pd.Series]: ...
    def plot_predict(self, start: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., end: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., dynamic: bool = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., exog_oos: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ..., fixed_oos: Union[None, np.ndarray, pd.DataFrame] = ..., alpha: float = ..., in_sample: bool = ..., fig: matplotlib.figure.Figure = ..., figsize: Optional[Tuple[int, int]] = ...) -> matplotlib.figure.Figure: ...
    def summary(self, alpha: float = ...) -> Summary: ...

class ARDLResultsWrapper(wrap.ResultsWrapper): ...

class ARDLOrderSelectionResults(AROrderSelectionResults):
    def __init__(self, model, ics, trend, seasonal, period): ...
    @property
    def dl_lags(self) -> Dict[Hashable, List[int]]: ...

def ardl_select_order(endog: Union[Sequence[float], pd.Series, _ArrayLike2D], maxlag: int, exog: _ArrayLike2D, maxorder: Union[int, Dict[Hashable, int]], trend: Any = ..., *, fixed: Optional[_ArrayLike2D] = ..., causal: bool = ..., ic: Literal[aic, bic] = ..., glob: bool = ..., seasonal: bool = ..., deterministic: Optional[DeterministicProcess] = ..., hold_back: Optional[int] = ..., period: Optional[int] = ..., missing: Any = ...) -> ARDLOrderSelectionResults: ...

class UECM(ARDL):
    def __init__(self, endog: Union[Sequence[float], pd.Series, _ArrayLike2D], lags: Union[None, int], exog: Optional[_ArrayLike2D] = ..., order: _UECMOrder = ..., trend: Any = ..., *, fixed: Optional[_ArrayLike2D] = ..., causal: bool = ..., seasonal: bool = ..., deterministic: Optional[DeterministicProcess] = ..., hold_back: Optional[int] = ..., period: Optional[int] = ..., missing: Any = ...) -> None: ...
    def fit(self, *, cov_type: str = ..., cov_kwds: Dict[str, Any] = ..., use_t: bool = ...) -> UECMResults: ...
    @classmethod
    def from_ardl(cls, ardl: ARDL, missing: Any = ...): ...
    def predict(self, params: Union[np.ndarray, pd.DataFrame], start: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., end: Union[None, int, str, dt.datetime, pd.Timestamp] = ..., dynamic: bool = ..., exog: Union[None, np.ndarray, pd.DataFrame] = ..., exog_oos: Union[None, np.ndarray, pd.DataFrame] = ..., fixed: Union[None, np.ndarray, pd.DataFrame] = ..., fixed_oos: Union[None, np.ndarray, pd.DataFrame] = ...) -> np.ndarray: ...
    @classmethod
    def from_formula(cls, formula: str, data: pd.DataFrame, lags: Union[None, int, Sequence[int]] = ..., order: _ARDLOrder = ..., trend: Any = ..., *, causal: bool = ..., seasonal: bool = ..., deterministic: Optional[DeterministicProcess] = ..., hold_back: Optional[int] = ..., period: Optional[int] = ..., missing: Any = ...) -> UECM: ...

class UECMResults(ARDLResults):
    def ci_params(self) -> Union[np.ndarray, pd.Series]: ...
    def ci_bse(self) -> Union[np.ndarray, pd.Series]: ...
    def ci_tvalues(self) -> Union[np.ndarray, pd.Series]: ...
    def ci_pvalues(self) -> Union[np.ndarray, pd.Series]: ...
    def ci_conf_int(self, alpha: float = ...) -> Union[np.ndarray, pd.DataFrame]: ...
    def ci_summary(self, alpha: float = ...) -> Summary: ...
    def ci_resids(self) -> Union[np.ndarray, pd.Series]: ...
    def ci_cov_params(self) -> Union[np.ndarray, pd.DataFrame]: ...
    def bounds_test(self, case: Any, cov_type: str = ..., cov_kwds: Dict[str, Any] = ..., use_t: bool = ..., asymptotic: bool = ..., nsim: int = ..., seed: Any = ...): ...

class UECMResultsWrapper(wrap.ResultsWrapper): ...
