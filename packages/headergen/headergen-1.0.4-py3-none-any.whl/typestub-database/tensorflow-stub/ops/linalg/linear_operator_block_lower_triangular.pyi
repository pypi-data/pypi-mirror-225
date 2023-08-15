from tensorflow.python.ops.linalg import linear_operator
from typing import Any

class LinearOperatorBlockLowerTriangular(linear_operator.LinearOperator):
    def __init__(self, operators, is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: Any | None = ..., name: str = ...) -> None: ...
    @property
    def operators(self): ...
    def matmul(self, x, adjoint: bool = ..., adjoint_arg: bool = ..., name: str = ...): ...
    def matvec(self, x, adjoint: bool = ..., name: str = ...): ...
    def solve(self, rhs, adjoint: bool = ..., adjoint_arg: bool = ..., name: str = ...): ...
    def solvevec(self, rhs, adjoint: bool = ..., name: str = ...): ...
