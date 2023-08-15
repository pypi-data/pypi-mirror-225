from .._docstrings import DocstringComponents as DocstringComponents
from typing import Any

EXAMPLE_DICT: Any

class ExampleClass:
    def example_method(self) -> None: ...

def example_func() -> None: ...

class TestDocstringComponents:
    def test_from_dict(self) -> None: ...
    def test_from_nested_components(self) -> None: ...
    def test_from_function(self) -> None: ...
    def test_from_method(self) -> None: ...
