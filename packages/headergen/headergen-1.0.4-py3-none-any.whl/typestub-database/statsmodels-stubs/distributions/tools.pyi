from typing import Any

class _Grid:
    k_grid: Any
    x_marginal: Any
    idx_flat: Any
    x_flat: Any
    def __init__(self, k_grid, eps: int = ...) -> None: ...

def prob2cdf_grid(probs): ...
def cdf2prob_grid(cdf, prepend: int = ...): ...
def average_grid(values, coords: Any | None = ..., _method: str = ...): ...
def nearest_matrix_margins(mat, maxiter: int = ..., tol: float = ...): ...
def frequencies_fromdata(data, k_bins, use_ranks: bool = ...): ...
def approx_copula_pdf(copula, k_bins: int = ..., force_uniform: bool = ...): ...
