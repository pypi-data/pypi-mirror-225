from matplotlib import docstring as docstring
from matplotlib.ticker import AutoLocator as AutoLocator, AutoMinorLocator as AutoMinorLocator, LogFormatterSciNotation as LogFormatterSciNotation, LogLocator as LogLocator, LogitFormatter as LogitFormatter, LogitLocator as LogitLocator, NullFormatter as NullFormatter, NullLocator as NullLocator, ScalarFormatter as ScalarFormatter, SymmetricalLogLocator as SymmetricalLogLocator
from matplotlib.transforms import IdentityTransform as IdentityTransform, Transform as Transform
from typing import Any

class ScaleBase:
    def __init__(self, axis) -> None: ...
    def get_transform(self) -> None: ...
    def set_default_locators_and_formatters(self, axis) -> None: ...
    def limit_range_for_scale(self, vmin, vmax, minpos): ...

class LinearScale(ScaleBase):
    name: str
    def __init__(self, axis) -> None: ...
    def set_default_locators_and_formatters(self, axis) -> None: ...
    def get_transform(self): ...

class FuncTransform(Transform):
    input_dims: int
    output_dims: int
    def __init__(self, forward, inverse) -> None: ...
    def transform_non_affine(self, values): ...
    def inverted(self): ...

class FuncScale(ScaleBase):
    name: str
    def __init__(self, axis, functions) -> None: ...
    def get_transform(self): ...
    def set_default_locators_and_formatters(self, axis) -> None: ...

class LogTransform(Transform):
    input_dims: int
    output_dims: int
    base: Any
    def __init__(self, base, nonpositive: str = ...) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class InvertedLogTransform(Transform):
    input_dims: int
    output_dims: int
    base: Any
    def __init__(self, base) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class LogScale(ScaleBase):
    name: str
    subs: Any
    def __init__(self, axis, *, base: int = ..., subs: Any | None = ..., nonpositive: str = ...) -> None: ...
    base: Any
    def set_default_locators_and_formatters(self, axis) -> None: ...
    def get_transform(self): ...
    def limit_range_for_scale(self, vmin, vmax, minpos): ...

class FuncScaleLog(LogScale):
    name: str
    subs: Any
    def __init__(self, axis, functions, base: int = ...) -> None: ...
    @property
    def base(self): ...
    def get_transform(self): ...

class SymmetricalLogTransform(Transform):
    input_dims: int
    output_dims: int
    base: Any
    linthresh: Any
    linscale: Any
    def __init__(self, base, linthresh, linscale) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class InvertedSymmetricalLogTransform(Transform):
    input_dims: int
    output_dims: int
    base: Any
    linthresh: Any
    invlinthresh: Any
    linscale: Any
    def __init__(self, base, linthresh, linscale) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class SymmetricalLogScale(ScaleBase):
    name: str
    subs: Any
    def __init__(self, axis, *, base: int = ..., linthresh: int = ..., subs: Any | None = ..., linscale: int = ...) -> None: ...
    base: Any
    linthresh: Any
    linscale: Any
    def set_default_locators_and_formatters(self, axis) -> None: ...
    def get_transform(self): ...

class LogitTransform(Transform):
    input_dims: int
    output_dims: int
    def __init__(self, nonpositive: str = ...) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class LogisticTransform(Transform):
    input_dims: int
    output_dims: int
    def __init__(self, nonpositive: str = ...) -> None: ...
    def transform_non_affine(self, a): ...
    def inverted(self): ...

class LogitScale(ScaleBase):
    name: str
    def __init__(self, axis, nonpositive: str = ..., *, one_half: str = ..., use_overline: bool = ...) -> None: ...
    def get_transform(self): ...
    def set_default_locators_and_formatters(self, axis) -> None: ...
    def limit_range_for_scale(self, vmin, vmax, minpos): ...

def get_scale_names(): ...
def scale_factory(scale, axis, **kwargs): ...
def register_scale(scale_class) -> None: ...
