import numpy as np
from datetime import timedelta
from pandas._config import config as config
from pandas._libs import lib as lib
from pandas._libs.tslibs import BaseOffset as BaseOffset, Period as Period, Tick as Tick, Timestamp as Timestamp, to_offset as to_offset
from pandas._typing import ArrayLike as ArrayLike, Axis as Axis, CompressionOptions as CompressionOptions, Dtype as Dtype, DtypeArg as DtypeArg, DtypeObj as DtypeObj, FilePath as FilePath, IndexKeyFunc as IndexKeyFunc, IndexLabel as IndexLabel, JSONSerializable as JSONSerializable, Level as Level, Manager as Manager, NDFrameT as NDFrameT, RandomState as RandomState, Renamer as Renamer, StorageOptions as StorageOptions, T as T, TimedeltaConvertibleTypes as TimedeltaConvertibleTypes, TimestampConvertibleTypes as TimestampConvertibleTypes, ValueKeyFunc as ValueKeyFunc, WriteBuffer as WriteBuffer, npt as npt
from pandas.compat._optional import import_optional_dependency as import_optional_dependency
from pandas.core import arraylike as arraylike, indexing as indexing, missing as missing, nanops as nanops
from pandas.core.array_algos.replace import should_use_regex as should_use_regex
from pandas.core.arrays import ExtensionArray as ExtensionArray
from pandas.core.base import PandasObject as PandasObject
from pandas.core.construction import create_series_with_explicit_dtype as create_series_with_explicit_dtype, extract_array as extract_array
from pandas.core.describe import describe_ndframe as describe_ndframe
from pandas.core.dtypes.common import ensure_object as ensure_object, ensure_platform_int as ensure_platform_int, ensure_str as ensure_str, is_bool as is_bool, is_bool_dtype as is_bool_dtype, is_datetime64_any_dtype as is_datetime64_any_dtype, is_datetime64tz_dtype as is_datetime64tz_dtype, is_dict_like as is_dict_like, is_dtype_equal as is_dtype_equal, is_extension_array_dtype as is_extension_array_dtype, is_float as is_float, is_list_like as is_list_like, is_number as is_number, is_numeric_dtype as is_numeric_dtype, is_re_compilable as is_re_compilable, is_scalar as is_scalar, is_timedelta64_dtype as is_timedelta64_dtype, pandas_dtype as pandas_dtype
from pandas.core.dtypes.generic import ABCDataFrame as ABCDataFrame, ABCSeries as ABCSeries
from pandas.core.dtypes.inference import is_hashable as is_hashable, is_nested_list_like as is_nested_list_like
from pandas.core.dtypes.missing import isna as isna, notna as notna
from pandas.core.flags import Flags as Flags
from pandas.core.frame import DataFrame as DataFrame
from pandas.core.indexers.objects import BaseIndexer as BaseIndexer
from pandas.core.indexes.api import DatetimeIndex as DatetimeIndex, Index as Index, MultiIndex as MultiIndex, PeriodIndex as PeriodIndex, RangeIndex as RangeIndex, default_index as default_index, ensure_index as ensure_index
from pandas.core.internals import ArrayManager as ArrayManager, BlockManager as BlockManager, SingleArrayManager as SingleArrayManager
from pandas.core.internals.construction import mgr_to_mgr as mgr_to_mgr
from pandas.core.missing import find_valid_index as find_valid_index
from pandas.core.ops import align_method_FRAME as align_method_FRAME
from pandas.core.resample import Resampler as Resampler
from pandas.core.reshape.concat import concat as concat
from pandas.core.series import Series as Series
from pandas.core.sorting import get_indexer_indexer as get_indexer_indexer
from pandas.core.window import Expanding as Expanding, ExponentialMovingWindow as ExponentialMovingWindow, Rolling as Rolling, Window as Window
from pandas.errors import AbstractMethodError as AbstractMethodError, InvalidIndexError as InvalidIndexError
from pandas.io.formats.format import DataFrameFormatter as DataFrameFormatter, DataFrameRenderer as DataFrameRenderer
from pandas.io.formats.printing import pprint_thing as pprint_thing
from pandas.util._decorators import doc as doc, rewrite_axis_style_signature as rewrite_axis_style_signature
from pandas.util._exceptions import find_stack_level as find_stack_level
from pandas.util._validators import validate_ascending as validate_ascending, validate_bool_kwarg as validate_bool_kwarg, validate_fillna_kwargs as validate_fillna_kwargs, validate_inclusive as validate_inclusive
from typing import Union, Any, Callable, Hashable, Literal, Mapping, Sequence, overload

bool_t = bool

class NDFrame(PandasObject, indexing.IndexingMixin):
    def __init__(self, data: Manager, copy: bool_t = ..., attrs: Union[Mapping[Hashable, Any], None] = ...) -> None: ...
    @property
    def attrs(self) -> dict[Hashable, Any]: ...
    @attrs.setter
    def attrs(self, value: Mapping[Hashable, Any]) -> None: ...
    @property
    def flags(self) -> Flags: ...
    def set_flags(self, *, copy: bool_t = ..., allows_duplicate_labels: Union[bool_t, None] = ...) -> NDFrameT: ...
    @property
    def shape(self) -> tuple[int, ...]: ...
    @property
    def axes(self) -> list[Index]: ...
    @property
    def ndim(self) -> int: ...
    @property
    def size(self) -> int: ...
    @overload
    def set_axis(self, labels, axis: Axis = ..., inplace: Literal[False] = ...) -> NDFrameT: ...
    @overload
    def set_axis(self, labels, axis: Axis, inplace: Literal[True]) -> None: ...
    @overload
    def set_axis(self, labels, inplace: Literal[True]) -> None: ...
    @overload
    def set_axis(self, labels, axis: Axis = ..., inplace: bool_t = ...) -> Union[NDFrameT, None]: ...
    def swapaxes(self, axis1, axis2, copy: bool = ...) -> NDFrameT: ...
    def droplevel(self, level, axis: int = ...) -> NDFrameT: ...
    def pop(self, item: Hashable) -> Union[Series, Any]: ...
    def squeeze(self, axis: Any | None = ...): ...
    def rename_axis(self, mapper=..., **kwargs): ...
    def equals(self, other: object) -> bool_t: ...
    def __neg__(self): ...
    def __pos__(self): ...
    def __invert__(self): ...
    def __nonzero__(self) -> None: ...
    __bool__: Any
    def bool(self): ...
    def abs(self) -> NDFrameT: ...
    def __abs__(self) -> NDFrameT: ...
    def __round__(self, decimals: int = ...) -> NDFrameT: ...
    __hash__: None
    def __iter__(self): ...
    def keys(self): ...
    def items(self) -> None: ...
    def iteritems(self): ...
    def __len__(self) -> int: ...
    def __contains__(self, key) -> bool_t: ...
    @property
    def empty(self) -> bool_t: ...
    __array_priority__: int
    def __array__(self, dtype: Union[npt.DTypeLike, None] = ...) -> np.ndarray: ...
    def __array_wrap__(self, result: np.ndarray, context: Union[tuple[Callable, tuple[Any, ...], int], None] = ...): ...
    def __array_ufunc__(self, ufunc: np.ufunc, method: str, *inputs: Any, **kwargs: Any): ...
    def to_excel(self, excel_writer, sheet_name: str = ..., na_rep: str = ..., float_format: Union[str, None] = ..., columns: Any | None = ..., header: bool = ..., index: bool = ..., index_label: Any | None = ..., startrow: int = ..., startcol: int = ..., engine: Any | None = ..., merge_cells: bool = ..., encoding: Any | None = ..., inf_rep: str = ..., verbose: bool = ..., freeze_panes: Any | None = ..., storage_options: StorageOptions = ...) -> None: ...
    def to_json(self, path_or_buf: Union[FilePath, WriteBuffer[bytes], WriteBuffer[str], None] = ..., orient: Union[str, None] = ..., date_format: Union[str, None] = ..., double_precision: int = ..., force_ascii: bool_t = ..., date_unit: str = ..., default_handler: Union[Callable[[Any], JSONSerializable], None] = ..., lines: bool_t = ..., compression: CompressionOptions = ..., index: bool_t = ..., indent: Union[int, None] = ..., storage_options: StorageOptions = ...) -> Union[str, None]: ...
    def to_hdf(self, path_or_buf, key: str, mode: str = ..., complevel: Union[int, None] = ..., complib: Union[str, None] = ..., append: bool_t = ..., format: Union[str, None] = ..., index: bool_t = ..., min_itemsize: Union[int, dict[str, int], None] = ..., nan_rep: Any | None = ..., dropna: Union[bool_t, None] = ..., data_columns: Union[Literal[True], list[str], None] = ..., errors: str = ..., encoding: str = ...) -> None: ...
    def to_sql(self, name: str, con, schema: Any | None = ..., if_exists: str = ..., index: bool_t = ..., index_label: Any | None = ..., chunksize: Any | None = ..., dtype: Union[DtypeArg, None] = ..., method: Any | None = ...) -> Union[int, None]: ...
    def to_pickle(self, path, compression: CompressionOptions = ..., protocol: int = ..., storage_options: StorageOptions = ...) -> None: ...
    def to_clipboard(self, excel: bool_t = ..., sep: Union[str, None] = ..., **kwargs) -> None: ...
    def to_xarray(self): ...
    def to_latex(self, buf: Any | None = ..., columns: Any | None = ..., col_space: Any | None = ..., header: bool = ..., index: bool = ..., na_rep: str = ..., formatters: Any | None = ..., float_format: Any | None = ..., sparsify: Any | None = ..., index_names: bool = ..., bold_rows: bool = ..., column_format: Any | None = ..., longtable: Any | None = ..., escape: Any | None = ..., encoding: Any | None = ..., decimal: str = ..., multicolumn: Any | None = ..., multicolumn_format: Any | None = ..., multirow: Any | None = ..., caption: Any | None = ..., label: Any | None = ..., position: Any | None = ...): ...
    def to_csv(self, path_or_buf: Union[FilePath, WriteBuffer[bytes], WriteBuffer[str], None] = ..., sep: str = ..., na_rep: str = ..., float_format: Union[str, None] = ..., columns: Union[Sequence[Hashable], None] = ..., header: Union[bool_t, list[str]] = ..., index: bool_t = ..., index_label: Union[IndexLabel, None] = ..., mode: str = ..., encoding: Union[str, None] = ..., compression: CompressionOptions = ..., quoting: Union[int, None] = ..., quotechar: str = ..., line_terminator: Union[str, None] = ..., chunksize: Union[int, None] = ..., date_format: Union[str, None] = ..., doublequote: bool_t = ..., escapechar: Union[str, None] = ..., decimal: str = ..., errors: str = ..., storage_options: StorageOptions = ...) -> Union[str, None]: ...
    def take(self, indices, axis: int = ..., is_copy: Union[bool_t, None] = ..., **kwargs) -> NDFrameT: ...
    def xs(self, key, axis: int = ..., level: Any | None = ..., drop_level: bool_t = ...): ...
    def __getitem__(self, item) -> None: ...
    def __delitem__(self, key) -> None: ...
    def get(self, key, default: Any | None = ...): ...
    def reindex_like(self, other, method: Union[str, None] = ..., copy: bool_t = ..., limit: Any | None = ..., tolerance: Any | None = ...) -> NDFrameT: ...
    def drop(self, labels: Any | None = ..., axis: int = ..., index: Any | None = ..., columns: Any | None = ..., level: Any | None = ..., inplace: bool_t = ..., errors: str = ...) -> NDFrameT: ...
    def add_prefix(self, prefix: str) -> NDFrameT: ...
    def add_suffix(self, suffix: str) -> NDFrameT: ...
    def sort_values(self, axis: int = ..., ascending: bool = ..., inplace: bool_t = ..., kind: str = ..., na_position: str = ..., ignore_index: bool_t = ..., key: ValueKeyFunc = ...): ...
    def sort_index(self, axis: int = ..., level: Any | None = ..., ascending: Union[bool_t, int, Sequence[Union[bool_t, int]]] = ..., inplace: bool_t = ..., kind: str = ..., na_position: str = ..., sort_remaining: bool_t = ..., ignore_index: bool_t = ..., key: IndexKeyFunc = ...): ...
    def reindex(self, *args, **kwargs) -> NDFrameT: ...
    def filter(self, items: Any | None = ..., like: Union[str, None] = ..., regex: Union[str, None] = ..., axis: Any | None = ...) -> NDFrameT: ...
    def head(self, n: int = ...) -> NDFrameT: ...
    def tail(self, n: int = ...) -> NDFrameT: ...
    def sample(self, n: Union[int, None] = ..., frac: Union[float, None] = ..., replace: bool_t = ..., weights: Any | None = ..., random_state: Union[RandomState, None] = ..., axis: Union[Axis, None] = ..., ignore_index: bool_t = ...) -> NDFrameT: ...
    def pipe(self, func: Union[Callable[..., T], tuple[Callable[..., T], str]], *args, **kwargs) -> T: ...
    def __finalize__(self, other, method: Union[str, None] = ..., **kwargs) -> NDFrameT: ...
    def __getattr__(self, name: str): ...
    def __setattr__(self, name: str, value) -> None: ...
    @property
    def values(self) -> np.ndarray: ...
    @property
    def dtypes(self): ...
    def astype(self, dtype, copy: bool_t = ..., errors: str = ...) -> NDFrameT: ...
    def copy(self, deep: bool_t = ...) -> NDFrameT: ...
    def __copy__(self, deep: bool_t = ...) -> NDFrameT: ...
    def __deepcopy__(self, memo: Any | None = ...) -> NDFrameT: ...
    def infer_objects(self) -> NDFrameT: ...
    def convert_dtypes(self, infer_objects: bool_t = ..., convert_string: bool_t = ..., convert_integer: bool_t = ..., convert_boolean: bool_t = ..., convert_floating: bool_t = ...) -> NDFrameT: ...
    def fillna(self, value: Any | None = ..., method: Any | None = ..., axis: Any | None = ..., inplace: bool_t = ..., limit: Any | None = ..., downcast: Any | None = ...) -> Union[NDFrameT, None]: ...
    def ffill(self, axis: Union[None, Axis] = ..., inplace: bool_t = ..., limit: Union[None, int] = ..., downcast: Any | None = ...) -> Union[NDFrameT, None]: ...
    pad: Any
    def bfill(self, axis: Union[None, Axis] = ..., inplace: bool_t = ..., limit: Union[None, int] = ..., downcast: Any | None = ...) -> Union[NDFrameT, None]: ...
    backfill: Any
    def replace(self, to_replace: Any | None = ..., value=..., inplace: bool_t = ..., limit: Union[int, None] = ..., regex: bool = ..., method=...): ...
    def interpolate(self, method: str = ..., axis: Axis = ..., limit: Union[int, None] = ..., inplace: bool_t = ..., limit_direction: Union[str, None] = ..., limit_area: Union[str, None] = ..., downcast: Union[str, None] = ..., **kwargs) -> Union[NDFrameT, None]: ...
    def asof(self, where, subset: Any | None = ...): ...
    def isna(self) -> NDFrameT: ...
    def isnull(self) -> NDFrameT: ...
    def notna(self) -> NDFrameT: ...
    def notnull(self) -> NDFrameT: ...
    def clip(self, lower: Any | None = ..., upper: Any | None = ..., axis: Union[Axis, None] = ..., inplace: bool_t = ..., *args, **kwargs) -> Union[NDFrameT, None]: ...
    def asfreq(self, freq, method: Any | None = ..., how: Union[str, None] = ..., normalize: bool_t = ..., fill_value: Any | None = ...) -> NDFrameT: ...
    def at_time(self, time, asof: bool_t = ..., axis: Any | None = ...) -> NDFrameT: ...
    def between_time(self, start_time, end_time, include_start: Union[bool_t, lib.NoDefault] = ..., include_end: Union[bool_t, lib.NoDefault] = ..., inclusive: Union[str, None] = ..., axis: Any | None = ...) -> NDFrameT: ...
    def resample(self, rule, axis: int = ..., closed: Union[str, None] = ..., label: Union[str, None] = ..., convention: str = ..., kind: Union[str, None] = ..., loffset: Any | None = ..., base: Union[int, None] = ..., on: Any | None = ..., level: Any | None = ..., origin: Union[str, TimestampConvertibleTypes] = ..., offset: Union[TimedeltaConvertibleTypes, None] = ...) -> Resampler: ...
    def first(self, offset) -> NDFrameT: ...
    def last(self, offset) -> NDFrameT: ...
    def rank(self, axis: int = ..., method: str = ..., numeric_only: Union[bool_t, None, lib.NoDefault] = ..., na_option: str = ..., ascending: bool_t = ..., pct: bool_t = ...) -> NDFrameT: ...
    def compare(self, other, align_axis: Axis = ..., keep_shape: bool_t = ..., keep_equal: bool_t = ...): ...
    def align(self, other, join: str = ..., axis: Any | None = ..., level: Any | None = ..., copy: bool = ..., fill_value: Any | None = ..., method: Any | None = ..., limit: Any | None = ..., fill_axis: int = ..., broadcast_axis: Any | None = ...): ...
    def where(self, cond, other=..., inplace: bool = ..., axis: Any | None = ..., level: Any | None = ..., errors: str = ..., try_cast=...): ...
    def mask(self, cond, other=..., inplace: bool = ..., axis: Any | None = ..., level: Any | None = ..., errors: str = ..., try_cast=...): ...
    def shift(self, periods: int = ..., freq: Any | None = ..., axis: int = ..., fill_value: Any | None = ...) -> NDFrameT: ...
    def slice_shift(self, periods: int = ..., axis: int = ...) -> NDFrameT: ...
    def tshift(self, periods: int = ..., freq: Any | None = ..., axis: Axis = ...) -> NDFrameT: ...
    def truncate(self, before: Any | None = ..., after: Any | None = ..., axis: Any | None = ..., copy: bool_t = ...) -> NDFrameT: ...
    def tz_convert(self, tz, axis: int = ..., level: Any | None = ..., copy: bool_t = ...) -> NDFrameT: ...
    def tz_localize(self, tz, axis: int = ..., level: Any | None = ..., copy: bool_t = ..., ambiguous: str = ..., nonexistent: str = ...) -> NDFrameT: ...
    def describe(self, percentiles: Any | None = ..., include: Any | None = ..., exclude: Any | None = ..., datetime_is_numeric: bool = ...) -> NDFrameT: ...
    def pct_change(self, periods: int = ..., fill_method: str = ..., limit: Any | None = ..., freq: Any | None = ..., **kwargs) -> NDFrameT: ...
    def any(self, axis: Axis = ..., bool_only: Union[bool_t, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., **kwargs) -> Union[Series, bool_t]: ...
    def all(self, axis: Axis = ..., bool_only: Union[bool_t, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., **kwargs) -> Union[Series, bool_t]: ...
    def cummax(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., *args, **kwargs): ...
    def cummin(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., *args, **kwargs): ...
    def cumsum(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., *args, **kwargs): ...
    def cumprod(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., *args, **kwargs): ...
    def sem(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., ddof: int = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def var(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., ddof: int = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def std(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., ddof: int = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def min(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs): ...
    def max(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs): ...
    def mean(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def median(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def skew(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    def kurt(self, axis: Union[Axis, None, lib.NoDefault] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., **kwargs) -> Union[Series, float]: ...
    kurtosis: Any
    def sum(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., min_count: int = ..., **kwargs): ...
    def prod(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ..., numeric_only: Union[bool_t, None] = ..., min_count: int = ..., **kwargs): ...
    product: Any
    def mad(self, axis: Union[Axis, None] = ..., skipna: bool_t = ..., level: Union[Level, None] = ...) -> Union[Series, float]: ...
    def rolling(self, window: Union[int, timedelta, BaseOffset, BaseIndexer], min_periods: Union[int, None] = ..., center: bool_t = ..., win_type: Union[str, None] = ..., on: Union[str, None] = ..., axis: Axis = ..., closed: Union[str, None] = ..., method: str = ...): ...
    def expanding(self, min_periods: int = ..., center: Union[bool_t, None] = ..., axis: Axis = ..., method: str = ...) -> Expanding: ...
    def ewm(self, com: Union[float, None] = ..., span: Union[float, None] = ..., halflife: Union[float, TimedeltaConvertibleTypes, None] = ..., alpha: Union[float, None] = ..., min_periods: Union[int, None] = ..., adjust: bool_t = ..., ignore_na: bool_t = ..., axis: Axis = ..., times: Union[str, np.ndarray, DataFrame, Series, None] = ..., method: str = ...) -> ExponentialMovingWindow: ...
    def __iadd__(self, other): ...
    def __isub__(self, other): ...
    def __imul__(self, other): ...
    def __itruediv__(self, other): ...
    def __ifloordiv__(self, other): ...
    def __imod__(self, other): ...
    def __ipow__(self, other): ...
    def __iand__(self, other): ...
    def __ior__(self, other): ...
    def __ixor__(self, other): ...
    def first_valid_index(self) -> Union[Hashable, None]: ...
    def last_valid_index(self) -> Union[Hashable, None]: ...
