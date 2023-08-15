import abc
from pandas import DataFrame as DataFrame, Index as Index, Series as Series
from pandas._config import option_context as option_context
from pandas._libs import lib as lib
from pandas._typing import AggFuncType as AggFuncType, AggFuncTypeBase as AggFuncTypeBase, AggFuncTypeDict as AggFuncTypeDict, AggObjType as AggObjType, Axis as Axis, NDFrameT as NDFrameT
from pandas.core.algorithms import safe_sort as safe_sort
from pandas.core.base import DataError as DataError, SelectionMixin as SelectionMixin, SpecificationError as SpecificationError
from pandas.core.construction import create_series_with_explicit_dtype as create_series_with_explicit_dtype, ensure_wrapped_if_datetimelike as ensure_wrapped_if_datetimelike
from pandas.core.dtypes.cast import is_nested_object as is_nested_object
from pandas.core.dtypes.common import is_dict_like as is_dict_like, is_extension_array_dtype as is_extension_array_dtype, is_list_like as is_list_like, is_sequence as is_sequence
from pandas.core.dtypes.generic import ABCDataFrame as ABCDataFrame, ABCNDFrame as ABCNDFrame, ABCSeries as ABCSeries
from pandas.core.groupby import GroupBy as GroupBy
from pandas.core.resample import Resampler as Resampler
from pandas.core.window.rolling import BaseWindow as BaseWindow
from pandas.util._decorators import cache_readonly as cache_readonly
from pandas.util._exceptions import find_stack_level as find_stack_level
from typing import Union, Any, Callable, Dict, Hashable, Iterable, Iterator

ResType = Dict[int, Any]

def frame_apply(obj: DataFrame, func: AggFuncType, axis: Axis = ..., raw: bool = ..., result_type: Union[str, None] = ..., args: Any | None = ..., kwargs: Any | None = ...) -> FrameApply: ...

class Apply(metaclass=abc.ABCMeta):
    axis: int
    obj: Any
    raw: Any
    args: Any
    kwargs: Any
    result_type: Any
    orig_f: Any
    f: Any
    def __init__(self, obj: AggObjType, func, raw: bool, result_type: Union[str, None], args, kwargs): ...
    @abc.abstractmethod
    def apply(self) -> Union[DataFrame, Series]: ...
    def agg(self) -> Union[DataFrame, Series, None]: ...
    def transform(self) -> Union[DataFrame, Series]: ...
    def transform_dict_like(self, func): ...
    def transform_str_or_callable(self, func) -> Union[DataFrame, Series]: ...
    def agg_list_like(self) -> Union[DataFrame, Series]: ...
    def agg_dict_like(self) -> Union[DataFrame, Series]: ...
    def apply_str(self) -> Union[DataFrame, Series]: ...
    def apply_multiple(self) -> Union[DataFrame, Series]: ...
    def normalize_dictlike_arg(self, how: str, obj: Union[DataFrame, Series], func: AggFuncTypeDict) -> AggFuncTypeDict: ...

class NDFrameApply(Apply, metaclass=abc.ABCMeta):
    @property
    def index(self) -> Index: ...
    @property
    def agg_axis(self) -> Index: ...

class FrameApply(NDFrameApply, metaclass=abc.ABCMeta):
    obj: DataFrame
    @property
    @abc.abstractmethod
    def result_index(self) -> Index: ...
    @property
    @abc.abstractmethod
    def result_columns(self) -> Index: ...
    @property
    @abc.abstractmethod
    def series_generator(self) -> Iterator[Series]: ...
    @abc.abstractmethod
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> Union[DataFrame, Series]: ...
    @property
    def res_columns(self) -> Index: ...
    @property
    def columns(self) -> Index: ...
    def values(self): ...
    def dtypes(self) -> Series: ...
    def apply(self) -> Union[DataFrame, Series]: ...
    axis: int
    def agg(self): ...
    def apply_empty_result(self): ...
    def apply_raw(self): ...
    def apply_broadcast(self, target: DataFrame) -> DataFrame: ...
    def apply_standard(self): ...
    def apply_series_generator(self) -> tuple[ResType, Index]: ...
    def wrap_results(self, results: ResType, res_index: Index) -> Union[DataFrame, Series]: ...
    def apply_str(self) -> Union[DataFrame, Series]: ...

class FrameRowApply(FrameApply):
    axis: int
    def apply_broadcast(self, target: DataFrame) -> DataFrame: ...
    @property
    def series_generator(self): ...
    @property
    def result_index(self) -> Index: ...
    @property
    def result_columns(self) -> Index: ...
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> Union[DataFrame, Series]: ...

class FrameColumnApply(FrameApply):
    axis: int
    def apply_broadcast(self, target: DataFrame) -> DataFrame: ...
    @property
    def series_generator(self) -> None: ...
    @property
    def result_index(self) -> Index: ...
    @property
    def result_columns(self) -> Index: ...
    def wrap_results_for_axis(self, results: ResType, res_index: Index) -> Union[DataFrame, Series]: ...
    def infer_to_same_shape(self, results: ResType, res_index: Index) -> DataFrame: ...

class SeriesApply(NDFrameApply):
    obj: Series
    axis: int
    convert_dtype: Any
    def __init__(self, obj: Series, func: AggFuncType, convert_dtype: bool, args, kwargs) -> None: ...
    def apply(self) -> Union[DataFrame, Series]: ...
    def agg(self): ...
    def apply_empty_result(self) -> Series: ...
    def apply_standard(self) -> Union[DataFrame, Series]: ...

class GroupByApply(Apply):
    axis: Any
    def __init__(self, obj: GroupBy[NDFrameT], func: AggFuncType, args, kwargs) -> None: ...
    def apply(self) -> None: ...
    def transform(self) -> None: ...

class ResamplerWindowApply(Apply):
    axis: int
    obj: Union[Resampler, BaseWindow]
    def __init__(self, obj: Union[Resampler, BaseWindow], func: AggFuncType, args, kwargs) -> None: ...
    def apply(self) -> None: ...
    def transform(self) -> None: ...

def reconstruct_func(func: Union[AggFuncType, None], **kwargs) -> tuple[bool, Union[AggFuncType, None], Union[list[str], None], Union[list[int], None]]: ...
def is_multi_agg_with_relabel(**kwargs) -> bool: ...
def normalize_keyword_aggregation(kwargs: dict) -> tuple[dict, list[str], list[int]]: ...
def relabel_result(result: Union[DataFrame, Series], func: dict[str, list[Union[Callable, str]]], columns: Iterable[Hashable], order: Iterable[int]) -> dict[Hashable, Series]: ...
def maybe_mangle_lambdas(agg_spec: Any) -> Any: ...
def validate_func_kwargs(kwargs: dict) -> tuple[list[str], list[Union[str, Callable[..., Any]]]]: ...
