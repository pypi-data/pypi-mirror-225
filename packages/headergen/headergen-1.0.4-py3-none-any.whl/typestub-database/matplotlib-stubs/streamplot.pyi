from typing import Any

def streamplot(axes, x, y, u, v, density: int = ..., linewidth: Any | None = ..., color: Any | None = ..., cmap: Any | None = ..., norm: Any | None = ..., arrowsize: int = ..., arrowstyle: str = ..., minlength: float = ..., transform: Any | None = ..., zorder: Any | None = ..., start_points: Any | None = ..., maxlength: float = ..., integration_direction: str = ...): ...

class StreamplotSet:
    lines: Any
    arrows: Any
    def __init__(self, lines, arrows) -> None: ...

class DomainMap:
    grid: Any
    mask: Any
    x_grid2mask: Any
    y_grid2mask: Any
    x_mask2grid: Any
    y_mask2grid: Any
    x_data2grid: Any
    y_data2grid: Any
    def __init__(self, grid, mask) -> None: ...
    def grid2mask(self, xi, yi): ...
    def mask2grid(self, xm, ym): ...
    def data2grid(self, xd, yd): ...
    def grid2data(self, xg, yg): ...
    def start_trajectory(self, xg, yg) -> None: ...
    def reset_start_point(self, xg, yg) -> None: ...
    def update_trajectory(self, xg, yg) -> None: ...
    def undo_trajectory(self) -> None: ...

class Grid:
    nx: Any
    ny: Any
    dx: Any
    dy: Any
    x_origin: Any
    y_origin: Any
    width: Any
    height: Any
    def __init__(self, x, y) -> None: ...
    @property
    def shape(self): ...
    def within_grid(self, xi, yi): ...

class StreamMask:
    shape: Any
    def __init__(self, density) -> None: ...
    def __getitem__(self, args): ...

class InvalidIndexError(Exception): ...
class TerminateTrajectory(Exception): ...
class OutOfBounds(IndexError): ...
