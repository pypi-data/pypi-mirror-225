from tensorflow.python.ops.distributions import distribution

class Dirichlet(distribution.Distribution):
    def __init__(self, concentration, validate_args: bool = ..., allow_nan_stats: bool = ..., name: str = ...) -> None: ...
    @property
    def concentration(self): ...
    @property
    def total_concentration(self): ...
