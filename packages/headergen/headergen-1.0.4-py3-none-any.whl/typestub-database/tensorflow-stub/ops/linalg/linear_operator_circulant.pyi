from tensorflow.python.ops.linalg import linear_operator
from typing import Any

class _BaseLinearOperatorCirculant(linear_operator.LinearOperator):
    def __init__(self, spectrum, block_depth, input_output_dtype=..., is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: bool = ..., parameters: Any | None = ..., name: str = ...) -> None: ...
    @property
    def block_depth(self): ...
    def block_shape_tensor(self): ...
    @property
    def block_shape(self): ...
    @property
    def spectrum(self): ...
    def convolution_kernel(self, name: str = ...): ...
    def assert_hermitian_spectrum(self, name: str = ...): ...

class LinearOperatorCirculant(_BaseLinearOperatorCirculant):
    def __init__(self, spectrum, input_output_dtype=..., is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: bool = ..., name: str = ...) -> None: ...

class LinearOperatorCirculant2D(_BaseLinearOperatorCirculant):
    def __init__(self, spectrum, input_output_dtype=..., is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: bool = ..., name: str = ...) -> None: ...

class LinearOperatorCirculant3D(_BaseLinearOperatorCirculant):
    def __init__(self, spectrum, input_output_dtype=..., is_non_singular: Any | None = ..., is_self_adjoint: Any | None = ..., is_positive_definite: Any | None = ..., is_square: bool = ..., name: str = ...) -> None: ...
