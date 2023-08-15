from statsmodels.tools.decorators import cache_readonly as cache_readonly
from typing import Any

class DescrStatsW:
    data: Any
    weights: Any
    ddof: Any
    def __init__(self, data, weights: Any | None = ..., ddof: int = ...) -> None: ...
    def sum_weights(self): ...
    def nobs(self): ...
    def sum(self): ...
    def mean(self): ...
    def demeaned(self): ...
    def sumsquares(self): ...
    def var_ddof(self, ddof: int = ...): ...
    def std_ddof(self, ddof: int = ...): ...
    def var(self): ...
    def std(self): ...
    def cov(self): ...
    def corrcoef(self): ...
    def std_mean(self): ...
    def quantile(self, probs, return_pandas: bool = ...): ...
    def tconfint_mean(self, alpha: float = ..., alternative: str = ...): ...
    def zconfint_mean(self, alpha: float = ..., alternative: str = ...): ...
    def ttest_mean(self, value: int = ..., alternative: str = ...): ...
    def ttost_mean(self, low, upp): ...
    def ztest_mean(self, value: int = ..., alternative: str = ...): ...
    def ztost_mean(self, low, upp): ...
    def get_compare(self, other, weights: Any | None = ...): ...
    def asrepeats(self): ...

class CompareMeans:
    d1: Any
    d2: Any
    def __init__(self, d1, d2) -> None: ...
    @classmethod
    def from_data(cls, data1, data2, weights1: Any | None = ..., weights2: Any | None = ..., ddof1: int = ..., ddof2: int = ...): ...
    def summary(self, use_t: bool = ..., alpha: float = ..., usevar: str = ..., value: int = ...): ...
    def std_meandiff_separatevar(self): ...
    def std_meandiff_pooledvar(self): ...
    def dof_satt(self): ...
    def ttest_ind(self, alternative: str = ..., usevar: str = ..., value: int = ...): ...
    def ztest_ind(self, alternative: str = ..., usevar: str = ..., value: int = ...): ...
    def tconfint_diff(self, alpha: float = ..., alternative: str = ..., usevar: str = ...): ...
    def zconfint_diff(self, alpha: float = ..., alternative: str = ..., usevar: str = ...): ...
    def ttost_ind(self, low, upp, usevar: str = ...): ...
    def ztost_ind(self, low, upp, usevar: str = ...): ...

def ttest_ind(x1, x2, alternative: str = ..., usevar: str = ..., weights=..., value: int = ...): ...
def ttost_ind(x1, x2, low, upp, usevar: str = ..., weights=..., transform: Any | None = ...): ...
def ttost_paired(x1, x2, low, upp, transform: Any | None = ..., weights: Any | None = ...): ...
def ztest(x1, x2: Any | None = ..., value: int = ..., alternative: str = ..., usevar: str = ..., ddof: float = ...): ...
def zconfint(x1, x2: Any | None = ..., value: int = ..., alpha: float = ..., alternative: str = ..., usevar: str = ..., ddof: float = ...): ...
def ztost(x1, low, upp, x2: Any | None = ..., usevar: str = ..., ddof: float = ...): ...
