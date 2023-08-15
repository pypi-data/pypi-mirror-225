from . import kernels as kernels
from statsmodels.compat.python import lzip as lzip
from statsmodels.tools.validation import array_like as array_like
from typing import Any

class KDE:
    kernel: Any
    n: Any
    x: Any
    def __init__(self, x, kernel: Any | None = ...) -> None: ...
    def density(self, x): ...
    def __call__(self, x, h: str = ...): ...
    def evaluate(self, x, h: str = ...): ...
