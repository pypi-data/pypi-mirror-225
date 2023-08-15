import statsmodels.base.model as base
from statsmodels.base._penalties import Penalty as Penalty
from statsmodels.tools.decorators import cache_readonly as cache_readonly
from statsmodels.tools.sm_exceptions import ConvergenceWarning as ConvergenceWarning
from typing import Any

class VCSpec:
    names: Any
    colnames: Any
    mats: Any
    def __init__(self, names, colnames, mats) -> None: ...

class MixedLMParams:
    k_fe: Any
    k_re: Any
    k_re2: Any
    k_vc: Any
    k_tot: Any
    def __init__(self, k_fe, k_re, k_vc) -> None: ...
    def from_packed(params, k_fe, k_re, use_sqrt, has_fe): ...
    def from_components(fe_params: Any | None = ..., cov_re: Any | None = ..., cov_re_sqrt: Any | None = ..., vcomp: Any | None = ...): ...
    def copy(self): ...
    def get_packed(self, use_sqrt, has_fe: bool = ...): ...

class MixedLM(base.LikelihoodModel):
    use_sqrt: Any
    reml: bool
    fe_pen: Any
    re_pen: Any
    k_vc: Any
    exog_vc: Any
    k_fe: Any
    k_re: int
    k_re2: int
    exog_re: Any
    k_params: Any
    row_indices: Any
    group_labels: Any
    n_groups: Any
    endog_li: Any
    exog_li: Any
    exog_re_li: Any
    exog_re2_li: Any
    nobs: Any
    n_totobs: Any
    exog_names: Any
    def __init__(self, endog, exog, groups, exog_re: Any | None = ..., exog_vc: Any | None = ..., use_sqrt: bool = ..., missing: str = ..., **kwargs) -> None: ...
    @classmethod
    def from_formula(cls, formula, data, re_formula: Any | None = ..., vc_formula: Any | None = ..., subset: Any | None = ..., use_sparse: bool = ..., missing: str = ..., *args, **kwargs): ...
    def predict(self, params, exog: Any | None = ...): ...
    def group_list(self, array): ...
    def fit_regularized(self, start_params: Any | None = ..., method: str = ..., alpha: int = ..., ceps: float = ..., ptol: float = ..., maxit: int = ..., **fit_kwargs): ...
    def get_fe_params(self, cov_re, vcomp, tol: float = ...): ...
    def loglike(self, params, profile_fe: bool = ...): ...
    def score(self, params, profile_fe: bool = ...): ...
    def score_full(self, params, calc_fe): ...
    def score_sqrt(self, params, calc_fe: bool = ...): ...
    def hessian(self, params): ...
    def get_scale(self, fe_params, cov_re, vcomp): ...
    cov_pen: Any
    def fit(self, start_params: Any | None = ..., reml: bool = ..., niter_sa: int = ..., do_cg: bool = ..., fe_pen: Any | None = ..., cov_pen: Any | None = ..., free: Any | None = ..., full_output: bool = ..., method: Any | None = ..., **fit_kwargs): ...
    def get_distribution(self, params, scale, exog): ...

class _mixedlm_distribution:
    model: Any
    exog: Any
    fe_params: Any
    cov_re: Any
    vcomp: Any
    scale: Any
    group_idx: Any
    def __init__(self, model, params, scale, exog) -> None: ...
    def rvs(self, n): ...

class MixedLMResults(base.LikelihoodModelResults, base.ResultMixin):
    nobs: Any
    df_resid: Any
    def __init__(self, model, params, cov_params) -> None: ...
    def fittedvalues(self): ...
    def resid(self): ...
    def bse_fe(self): ...
    def bse_re(self): ...
    def random_effects(self): ...
    def random_effects_cov(self): ...
    def t_test(self, r_matrix, use_t: Any | None = ...): ...
    def summary(self, yname: Any | None = ..., xname_fe: Any | None = ..., xname_re: Any | None = ..., title: Any | None = ..., alpha: float = ...): ...
    def llf(self): ...
    def aic(self): ...
    def bic(self): ...
    def profile_re(self, re_ix, vtype, num_low: int = ..., dist_low: float = ..., num_high: int = ..., dist_high: float = ..., **fit_kwargs): ...

class MixedLMResultsWrapper(base.LikelihoodResultsWrapper): ...
