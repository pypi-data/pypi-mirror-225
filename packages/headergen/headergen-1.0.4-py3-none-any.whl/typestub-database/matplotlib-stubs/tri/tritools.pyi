from matplotlib.tri import Triangulation as Triangulation

class TriAnalyzer:
    def __init__(self, triangulation) -> None: ...
    @property
    def scale_factors(self): ...
    def circle_ratios(self, rescale: bool = ...): ...
    def get_flat_tri_mask(self, min_circle_ratio: float = ..., rescale: bool = ...): ...
