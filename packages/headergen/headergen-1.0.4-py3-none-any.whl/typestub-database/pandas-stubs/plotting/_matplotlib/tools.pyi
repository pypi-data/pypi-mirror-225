import numpy as np
from matplotlib.axes import Axes as Axes
from matplotlib.axis import Axis as Axis
from matplotlib.figure import Figure as Figure
from matplotlib.lines import Line2D as Line2D
from matplotlib.table import Table as Table
from pandas.core.frame import DataFrame as DataFrame, Series as Series
from pandas.core.dtypes.common import is_list_like as is_list_like
from pandas.core.dtypes.generic import ABCDataFrame as ABCDataFrame, ABCIndex as ABCIndex, ABCSeries as ABCSeries
from pandas.plotting._matplotlib import compat as compat
from pandas.util._exceptions import find_stack_level as find_stack_level
from typing import Union, Any, Iterable, Sequence

def do_adjust_figure(fig: Figure): ...
def maybe_adjust_figure(fig: Figure, *args, **kwargs): ...
def format_date_labels(ax: Axes, rot): ...
def table(ax, data: Union[DataFrame, Series], rowLabels: Any | None = ..., colLabels: Any | None = ..., **kwargs) -> Table: ...
def create_subplots(naxes: int, sharex: bool = ..., sharey: bool = ..., squeeze: bool = ..., subplot_kw: Any | None = ..., ax: Any | None = ..., layout: Any | None = ..., layout_type: str = ..., **fig_kw): ...
def handle_shared_axes(axarr: Iterable[Axes], nplots: int, naxes: int, nrows: int, ncols: int, sharex: bool, sharey: bool): ...
def flatten_axes(axes: Union[Axes, Sequence[Axes]]) -> np.ndarray: ...
def set_ticks_props(axes: Union[Axes, Sequence[Axes]], xlabelsize: Any | None = ..., xrot: Any | None = ..., ylabelsize: Any | None = ..., yrot: Any | None = ...): ...
def get_all_lines(ax: Axes) -> list[Line2D]: ...
def get_xlim(lines: Iterable[Line2D]) -> tuple[float, float]: ...
