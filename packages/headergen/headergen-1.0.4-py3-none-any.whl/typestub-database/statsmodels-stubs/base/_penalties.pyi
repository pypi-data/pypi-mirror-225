from typing import Any

class Penalty:
    weights: Any
    alpha: float
    def __init__(self, weights: float = ...) -> None: ...
    def func(self, params) -> None: ...
    def deriv(self, params) -> None: ...

class NonePenalty(Penalty):
    def __init__(self, **kwds) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class L2(Penalty):
    def __init__(self, weights: float = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class L2Univariate(Penalty):
    weights: float
    def __init__(self, weights: Any | None = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class PseudoHuber(Penalty):
    dlt: Any
    def __init__(self, dlt, weights: float = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class SCAD(Penalty):
    tau: Any
    c: Any
    def __init__(self, tau, c: float = ..., weights: float = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class SCADSmoothed(SCAD):
    tau: Any
    c: Any
    c0: Any
    weights: float
    aq1: Any
    aq2: Any
    restriction: Any
    def __init__(self, tau, c: float = ..., c0: Any | None = ..., weights: float = ..., restriction: Any | None = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    def deriv2(self, params): ...

class ConstraintsPenalty:
    penalty: Any
    weights: float
    restriction: Any
    def __init__(self, penalty, weights: Any | None = ..., restriction: Any | None = ...) -> None: ...
    def func(self, params): ...
    def deriv(self, params): ...
    grad: Any
    def deriv2(self, params): ...

class L2ConstraintsPenalty(ConstraintsPenalty):
    def __init__(self, weights: Any | None = ..., restriction: Any | None = ..., sigma_prior: Any | None = ...) -> None: ...

class CovariancePenalty:
    weight: Any
    def __init__(self, weight) -> None: ...
    def func(self, mat, mat_inv) -> None: ...
    def deriv(self, mat, mat_inv) -> None: ...

class PSD(CovariancePenalty):
    def func(self, mat, mat_inv): ...
    def deriv(self, mat, mat_inv): ...
