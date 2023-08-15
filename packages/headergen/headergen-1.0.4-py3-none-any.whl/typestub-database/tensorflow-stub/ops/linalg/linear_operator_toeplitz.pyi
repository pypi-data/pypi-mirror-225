from tensorflow.python.ops.linalg import linear_operator
from typing import Any

class LinearOperatorToeplitz(linear_operator.LinearOperator):
    def __init__(self, col, row, is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: Any | None = ..., name: str = ...) -> None: ...
    @property
    def col(self): ...
    @property
    def row(self): ...
