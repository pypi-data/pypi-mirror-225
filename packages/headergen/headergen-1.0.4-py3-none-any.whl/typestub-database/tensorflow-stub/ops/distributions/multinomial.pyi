from tensorflow.python.ops.distributions import distribution
from typing import Any

class Multinomial(distribution.Distribution):
    def __init__(self, total_count, logits: Any | None = ..., probs: Any | None = ..., validate_args: bool = ..., allow_nan_stats: bool = ..., name: str = ...) -> None: ...
    @property
    def total_count(self): ...
    @property
    def logits(self): ...
    @property
    def probs(self): ...
