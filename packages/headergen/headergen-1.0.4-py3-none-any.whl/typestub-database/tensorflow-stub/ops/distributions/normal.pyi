from tensorflow.python.ops.distributions import distribution

class Normal(distribution.Distribution):
    def __init__(self, loc, scale, validate_args: bool = ..., allow_nan_stats: bool = ..., name: str = ...) -> None: ...
    @property
    def loc(self): ...
    @property
    def scale(self): ...

class NormalWithSoftplusScale(Normal):
    def __init__(self, loc, scale, validate_args: bool = ..., allow_nan_stats: bool = ..., name: str = ...) -> None: ...
