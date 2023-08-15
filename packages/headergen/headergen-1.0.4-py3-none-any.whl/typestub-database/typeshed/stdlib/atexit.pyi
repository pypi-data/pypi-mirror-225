from collections.abc import Callable
from typing import TypeVar
from typing_extensions import ParamSpec

_T = TypeVar("_T")
_P = ParamSpec("_P")

def _clear() -> None: ...
def _ncallbacks() -> int: ...
def _run_exitfuncs() -> None: ...
def register(func: Callable[_P, _T], *args: _P.args, **kwargs: _P.kwargs) -> Callable[_P, _T]: ...
def unregister(func: Callable[..., object]) -> None: ...
