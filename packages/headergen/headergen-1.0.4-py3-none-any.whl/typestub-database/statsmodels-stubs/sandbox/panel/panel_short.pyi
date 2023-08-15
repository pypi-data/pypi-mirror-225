from statsmodels.regression.linear_model import GLS as GLS, OLS as OLS
from statsmodels.tools.grouputils import GroupSorted as GroupSorted
from typing import Any

def sum_outer_product_loop(x, group_iter): ...
def sum_outer_product_balanced(x, n_groups): ...
def whiten_individuals_loop(x, transform, group_iter): ...

class ShortPanelGLS2:
    endog: Any
    exog: Any
    group: Any
    n_groups: Any
    def __init__(self, endog, exog, group) -> None: ...
    res_pooled: Any
    def fit_ols(self): ...
    def get_within_cov(self, resid): ...
    def whiten_groups(self, x, cholsigmainv_i): ...
    cholsigmainv_i: Any
    res1: Any
    def fit(self): ...

class ShortPanelGLS(GLS):
    group: Any
    n_groups: Any
    cholsigmainv_i: Any
    def __init__(self, endog, exog, group, sigma_i: Any | None = ...) -> None: ...
    def get_within_cov(self, resid): ...
    def whiten_groups(self, x, cholsigmainv_i): ...
    def whiten(self, x): ...
    history: Any
    results_old: Any
    def fit_iterative(self, maxiter: int = ...): ...
