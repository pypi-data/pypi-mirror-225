from scipy.stats import distributions
from statsmodels.stats.moment_helpers import mc2mvsk as mc2mvsk, mvsk2mc as mvsk2mc
from typing import Any

class SkewNorm_gen(distributions.rv_continuous):
    def __init__(self) -> None: ...

skewnorm: Any

class SkewNorm2_gen(distributions.rv_continuous): ...

skewnorm2: Any

class ACSkewT_gen(distributions.rv_continuous):
    def __init__(self) -> None: ...

def pdf_moments_st(cnt): ...
def pdf_mvsk(mvsk): ...
def pdf_moments(cnt): ...

class NormExpan_gen(distributions.rv_continuous):
    mvsk: Any
    cnt: Any
    def __init__(self, args, **kwds) -> None: ...

def get_u_argskwargs(**kwargs): ...

class Transf_gen(distributions.rv_continuous):
    func: Any
    funcinv: Any
    numargs: Any
    decr: Any
    kls: Any
    def __init__(self, kls, func, funcinv, *args, **kwargs) -> None: ...

def inverse(x): ...

mux: Any
stdx: Any

def inversew(x): ...
def inversew_inv(x): ...
def identit(x): ...

invdnormalg: Any
lognormalg: Any
loggammaexpg: Any

class ExpTransf_gen(distributions.rv_continuous):
    numargs: Any
    kls: Any
    def __init__(self, kls, *args, **kwargs) -> None: ...

class LogTransf_gen(distributions.rv_continuous):
    numargs: Any
    kls: Any
    def __init__(self, kls, *args, **kwargs) -> None: ...

class TransfTwo_gen(distributions.rv_continuous):
    func: Any
    funcinvplus: Any
    funcinvminus: Any
    derivplus: Any
    derivminus: Any
    numargs: Any
    shape: Any
    kls: Any
    def __init__(self, kls, func, funcinvplus, funcinvminus, derivplus, derivminus, *args, **kwargs) -> None: ...

class SquareFunc:
    def inverseplus(self, x): ...
    def inverseminus(self, x): ...
    def derivplus(self, x): ...
    def derivminus(self, x): ...
    def squarefunc(self, x): ...

sqfunc: Any
squarenormalg: Any
squaretg: Any

def inverseplus(x): ...
def inverseminus(x): ...
def derivplus(x): ...
def derivminus(x): ...
def negsquarefunc(x): ...

negsquarenormalg: Any

def absfunc(x): ...

absnormalg: Any
informcode: Any

def mvstdnormcdf(lower, upper, corrcoef, **kwds): ...
def mvnormcdf(upper, mu, cov, lower: Any | None = ..., **kwds): ...
