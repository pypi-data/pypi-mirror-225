import statsmodels.base.model as base
from statsmodels.genmod import families as families
from statsmodels.iolib import summary2 as summary2
from typing import Any

glw: Any

class _BayesMixedGLM(base.Model):
    exog_vc: Any
    exog_vc2: Any
    ident: Any
    family: Any
    k_fep: Any
    k_vc: Any
    k_vcp: Any
    fep_names: Any
    vcp_names: Any
    vc_names: Any
    fe_p: Any
    vcp_p: Any
    names: Any
    def __init__(self, endog, exog, exog_vc: Any | None = ..., ident: Any | None = ..., family: Any | None = ..., vcp_p: int = ..., fe_p: int = ..., fep_names: Any | None = ..., vcp_names: Any | None = ..., vc_names: Any | None = ..., **kwargs) -> None: ...
    def logposterior(self, params): ...
    def logposterior_grad(self, params): ...
    @classmethod
    def from_formula(cls, formula, vc_formulas, data, family: Any | None = ..., vcp_p: int = ..., fe_p: int = ...): ...
    def fit(self, method: str = ..., minim_opts: Any | None = ...) -> None: ...
    exog: Any
    def fit_map(self, method: str = ..., minim_opts: Any | None = ..., scale_fe: bool = ...): ...
    def predict(self, params, exog: Any | None = ..., linear: bool = ...): ...

class _VariationalBayesMixedGLM:
    rng: int
    verbose: bool
    def vb_elbo_base(self, h, tm, fep_mean, vcp_mean, vc_mean, fep_sd, vcp_sd, vc_sd): ...
    def vb_elbo_grad_base(self, h, tm, tv, fep_mean, vcp_mean, vc_mean, fep_sd, vcp_sd, vc_sd): ...
    exog: Any
    def fit_vb(self, mean: Any | None = ..., sd: Any | None = ..., fit_method: str = ..., minim_opts: Any | None = ..., scale_fe: bool = ..., verbose: bool = ...): ...

class BayesMixedGLMResults:
    model: Any
    params: Any
    optim_retvals: Any
    fe_sd: Any
    vcp_sd: Any
    vc_sd: Any
    def __init__(self, model, params, cov_params, optim_retvals: Any | None = ...) -> None: ...
    def cov_params(self): ...
    def summary(self): ...
    def random_effects(self, term: Any | None = ...): ...
    def predict(self, exog: Any | None = ..., linear: bool = ...): ...

class BinomialBayesMixedGLM(_VariationalBayesMixedGLM, _BayesMixedGLM):
    __doc__: Any
    def __init__(self, endog, exog, exog_vc, ident, vcp_p: int = ..., fe_p: int = ..., fep_names: Any | None = ..., vcp_names: Any | None = ..., vc_names: Any | None = ...) -> None: ...
    @classmethod
    def from_formula(cls, formula, vc_formulas, data, vcp_p: int = ..., fe_p: int = ...): ...
    def vb_elbo(self, vb_mean, vb_sd): ...
    def vb_elbo_grad(self, vb_mean, vb_sd): ...

class PoissonBayesMixedGLM(_VariationalBayesMixedGLM, _BayesMixedGLM):
    __doc__: Any
    def __init__(self, endog, exog, exog_vc, ident, vcp_p: int = ..., fe_p: int = ..., fep_names: Any | None = ..., vcp_names: Any | None = ..., vc_names: Any | None = ...) -> None: ...
    @classmethod
    def from_formula(cls, formula, vc_formulas, data, vcp_p: int = ..., fe_p: int = ..., vcp_names: Any | None = ..., vc_names: Any | None = ...): ...
    def vb_elbo(self, vb_mean, vb_sd): ...
    def vb_elbo_grad(self, vb_mean, vb_sd): ...
