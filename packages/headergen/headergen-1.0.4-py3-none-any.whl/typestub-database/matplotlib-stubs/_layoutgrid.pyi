from matplotlib.transforms import Bbox as Bbox
from typing import Any

class LayoutGrid:
    parent: Any
    parent_pos: Any
    parent_inner: Any
    name: Any
    nrows: Any
    ncols: Any
    height_ratios: Any
    width_ratios: Any
    solver: Any
    artists: Any
    children: Any
    margins: Any
    margin_vals: Any
    widths: Any
    lefts: Any
    rights: Any
    inner_widths: Any
    heights: Any
    inner_heights: Any
    bottoms: Any
    tops: Any
    h_pad: Any
    w_pad: Any
    def __init__(self, parent: Any | None = ..., parent_pos=..., parent_inner: bool = ..., name: str = ..., ncols: int = ..., nrows: int = ..., h_pad: Any | None = ..., w_pad: Any | None = ..., width_ratios: Any | None = ..., height_ratios: Any | None = ...) -> None: ...
    def reset_margins(self) -> None: ...
    def add_constraints(self) -> None: ...
    def hard_constraints(self) -> None: ...
    def add_child(self, child, i: int = ..., j: int = ...) -> None: ...
    def parent_constraints(self) -> None: ...
    def grid_constraints(self) -> None: ...
    def edit_margin(self, todo, size, cell) -> None: ...
    def edit_margin_min(self, todo, size, cell: int = ...) -> None: ...
    def edit_margins(self, todo, size) -> None: ...
    def edit_all_margins_min(self, todo, size) -> None: ...
    def edit_outer_margin_mins(self, margin, ss) -> None: ...
    def get_margins(self, todo, col): ...
    def get_outer_bbox(self, rows: int = ..., cols: int = ...): ...
    def get_inner_bbox(self, rows: int = ..., cols: int = ...): ...
    def get_bbox_for_cb(self, rows: int = ..., cols: int = ...): ...
    def get_left_margin_bbox(self, rows: int = ..., cols: int = ...): ...
    def get_bottom_margin_bbox(self, rows: int = ..., cols: int = ...): ...
    def get_right_margin_bbox(self, rows: int = ..., cols: int = ...): ...
    def get_top_margin_bbox(self, rows: int = ..., cols: int = ...): ...
    def update_variables(self) -> None: ...

def seq_id(): ...
def print_children(lb) -> None: ...
def plot_children(fig, lg: Any | None = ..., level: int = ..., printit: bool = ...) -> None: ...
