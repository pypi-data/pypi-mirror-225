import abc
from tensorflow.python.framework import composite_tensor, type_spec
from tensorflow.python.module import module
from typing import Any

class LinearOperator(module.Module, composite_tensor.CompositeTensor, metaclass=abc.ABCMeta):
    def __init__(self, dtype, graph_parents: Any | None = ..., is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: Any | None = ..., name: Any | None = ..., parameters: Any | None = ...) -> None: ...
    def parameters(self): ...
    def dtype(self): ...
    def name(self): ...
    def graph_parents(self): ...
    def is_non_singular(self): ...
    def is_self_adjoint(self): ...
    def is_positive_definite(self): ...
    def is_square(self): ...
    def shape(self): ...
    def shape_tensor(self, name: str = ...): ...
    def batch_shape(self): ...
    def batch_shape_tensor(self, name: str = ...): ...
    def tensor_rank(self, name: str = ...): ...
    def tensor_rank_tensor(self, name: str = ...): ...
    def domain_dimension(self): ...
    def domain_dimension_tensor(self, name: str = ...): ...
    def range_dimension(self): ...
    def range_dimension_tensor(self, name: str = ...): ...
    def assert_non_singular(self, name: str = ...): ...
    def assert_positive_definite(self, name: str = ...): ...
    def assert_self_adjoint(self, name: str = ...): ...
    def matmul(self, x, adjoint: bool = ..., adjoint_arg: bool = ..., name: str = ...): ...
    def __matmul__(self, other): ...
    def matvec(self, x, adjoint: bool = ..., name: str = ...): ...
    def determinant(self, name: str = ...): ...
    def log_abs_determinant(self, name: str = ...): ...
    def solve(self, rhs, adjoint: bool = ..., adjoint_arg: bool = ..., name: str = ...): ...
    def solvevec(self, rhs, adjoint: bool = ..., name: str = ...): ...
    def adjoint(self, name: str = ...): ...
    H: Any
    def inverse(self, name: str = ...): ...
    def cholesky(self, name: str = ...): ...
    def to_dense(self, name: str = ...): ...
    def diag_part(self, name: str = ...): ...
    def trace(self, name: str = ...): ...
    def add_to_tensor(self, x, name: str = ...): ...
    def eigvals(self, name: str = ...): ...
    def cond(self, name: str = ...): ...

class _LinearOperatorSpec(type_spec.TypeSpec):
    def __init__(self, param_specs, non_tensor_params, prefer_static_fields) -> None: ...
    @classmethod
    def from_operator(cls, operator): ...
