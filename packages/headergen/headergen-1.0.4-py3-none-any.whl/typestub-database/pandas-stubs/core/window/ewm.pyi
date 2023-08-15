import numpy as np
from pandas.core.frame import DataFrame as DataFrame, Series as Series
from pandas._libs.tslibs import Timedelta as Timedelta
from pandas._typing import Axis as Axis, TimedeltaConvertibleTypes as TimedeltaConvertibleTypes
from pandas.core.dtypes.common import is_datetime64_ns_dtype as is_datetime64_ns_dtype
from pandas.core.dtypes.missing import isna as isna
from pandas.core.generic import NDFrame as NDFrame
from pandas.core.indexers.objects import BaseIndexer as BaseIndexer, ExponentialMovingWindowIndexer as ExponentialMovingWindowIndexer, GroupbyIndexer as GroupbyIndexer
from pandas.core.util.numba_ import maybe_use_numba as maybe_use_numba
from pandas.core.window.common import zsqrt as zsqrt
from pandas.core.window.doc import args_compat as args_compat, create_section_header as create_section_header, kwargs_compat as kwargs_compat, numba_notes as numba_notes, template_header as template_header, template_returns as template_returns, template_see_also as template_see_also, window_agg_numba_parameters as window_agg_numba_parameters
from pandas.core.window.numba_ import generate_numba_ewm_func as generate_numba_ewm_func, generate_numba_ewm_table_func as generate_numba_ewm_table_func
from pandas.core.window.online import EWMMeanState as EWMMeanState, generate_online_numba_ewma_func as generate_online_numba_ewma_func
from pandas.core.window.rolling import BaseWindow as BaseWindow, BaseWindowGroupby as BaseWindowGroupby
from pandas.util._decorators import doc as doc
from pandas.util._exceptions import find_stack_level as find_stack_level
from typing import Union, Any

def get_center_of_mass(comass: Union[float, None], span: Union[float, None], halflife: Union[float, None], alpha: Union[float, None]) -> float: ...

class ExponentialMovingWindow(BaseWindow):
    com: Any
    span: Any
    halflife: Any
    alpha: Any
    adjust: Any
    ignore_na: Any
    times: Any
    def __init__(self, obj: NDFrame, com: Union[float, None] = ..., span: Union[float, None] = ..., halflife: Union[float, TimedeltaConvertibleTypes, None] = ..., alpha: Union[float, None] = ..., min_periods: Union[int, None] = ..., adjust: bool = ..., ignore_na: bool = ..., axis: Axis = ..., times: Union[str, np.ndarray, NDFrame, None] = ..., method: str = ..., *, selection: Any | None = ...) -> None: ...
    def online(self, engine: str = ..., engine_kwargs: Any | None = ...): ...
    def aggregate(self, func, *args, **kwargs): ...
    agg: Any
    def mean(self, *args, engine: Any | None = ..., engine_kwargs: Any | None = ..., **kwargs): ...
    def sum(self, *args, engine: Any | None = ..., engine_kwargs: Any | None = ..., **kwargs): ...
    def std(self, bias: bool = ..., *args, **kwargs): ...
    def vol(self, bias: bool = ..., *args, **kwargs): ...
    def var(self, bias: bool = ..., *args, **kwargs): ...
    def cov(self, other: Union[DataFrame, Series, None] = ..., pairwise: Union[bool, None] = ..., bias: bool = ..., **kwargs): ...
    def corr(self, other: Union[DataFrame, Series, None] = ..., pairwise: Union[bool, None] = ..., **kwargs): ...

class ExponentialMovingWindowGroupby(BaseWindowGroupby, ExponentialMovingWindow):
    def __init__(self, obj, *args, _grouper: Any | None = ..., **kwargs) -> None: ...

class OnlineExponentialMovingWindow(ExponentialMovingWindow):
    engine: Any
    engine_kwargs: Any
    def __init__(self, obj: NDFrame, com: Union[float, None] = ..., span: Union[float, None] = ..., halflife: Union[float, TimedeltaConvertibleTypes, None] = ..., alpha: Union[float, None] = ..., min_periods: Union[int, None] = ..., adjust: bool = ..., ignore_na: bool = ..., axis: Axis = ..., times: Union[str, np.ndarray, NDFrame, None] = ..., engine: str = ..., engine_kwargs: Union[dict[str, bool], None] = ..., *, selection: Any | None = ...) -> None: ...
    def reset(self) -> None: ...
    def aggregate(self, func, *args, **kwargs): ...
    def std(self, bias: bool = ..., *args, **kwargs): ...
    def corr(self, other: Union[DataFrame, Series, None] = ..., pairwise: Union[bool, None] = ..., **kwargs): ...
    def cov(self, other: Union[DataFrame, Series, None] = ..., pairwise: Union[bool, None] = ..., bias: bool = ..., **kwargs): ...
    def var(self, bias: bool = ..., *args, **kwargs): ...
    def mean(self, *args, update: Any | None = ..., update_times: Any | None = ..., **kwargs): ...
