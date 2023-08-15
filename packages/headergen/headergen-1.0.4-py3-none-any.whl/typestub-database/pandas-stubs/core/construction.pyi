import numpy.ma as ma
import numpy as np
from pandas import ExtensionArray as ExtensionArray, Index as Index, Series as Series
from pandas._libs import lib as lib
from pandas._typing import AnyArrayLike as AnyArrayLike, ArrayLike as ArrayLike, Dtype as Dtype, DtypeObj as DtypeObj
from pandas.core.dtypes.base import ExtensionDtype as ExtensionDtype
from pandas.core.dtypes.cast import construct_1d_arraylike_from_scalar as construct_1d_arraylike_from_scalar, construct_1d_object_array_from_listlike as construct_1d_object_array_from_listlike, maybe_cast_to_datetime as maybe_cast_to_datetime, maybe_cast_to_integer_array as maybe_cast_to_integer_array, maybe_convert_platform as maybe_convert_platform, maybe_infer_to_datetimelike as maybe_infer_to_datetimelike, maybe_upcast as maybe_upcast, sanitize_to_nanoseconds as sanitize_to_nanoseconds
from pandas.core.dtypes.common import is_datetime64_ns_dtype as is_datetime64_ns_dtype, is_extension_array_dtype as is_extension_array_dtype, is_float_dtype as is_float_dtype, is_integer_dtype as is_integer_dtype, is_list_like as is_list_like, is_object_dtype as is_object_dtype, is_timedelta64_ns_dtype as is_timedelta64_ns_dtype
from pandas.core.dtypes.dtypes import DatetimeTZDtype as DatetimeTZDtype, PandasDtype as PandasDtype
from pandas.core.dtypes.generic import ABCExtensionArray as ABCExtensionArray, ABCIndex as ABCIndex, ABCPandasArray as ABCPandasArray, ABCRangeIndex as ABCRangeIndex, ABCSeries as ABCSeries
from pandas.core.dtypes.missing import isna as isna
from pandas.errors import IntCastingNaNError as IntCastingNaNError
from pandas.util._exceptions import find_stack_level as find_stack_level
from typing import Union, Any, Sequence

def array(data: Union[Sequence[object], AnyArrayLike], dtype: Union[Dtype, None] = ..., copy: bool = ...) -> ExtensionArray: ...
def extract_array(obj: object, extract_numpy: bool = ..., extract_range: bool = ...) -> Union[Any, ArrayLike]: ...
def ensure_wrapped_if_datetimelike(arr): ...
def sanitize_masked_array(data: ma.MaskedArray) -> np.ndarray: ...
def sanitize_array(data, index: Union[Index, None], dtype: Union[DtypeObj, None] = ..., copy: bool = ..., raise_cast_failure: bool = ..., *, allow_2d: bool = ...) -> ArrayLike: ...
def range_to_ndarray(rng: range) -> np.ndarray: ...
def is_empty_data(data: Any) -> bool: ...
def create_series_with_explicit_dtype(data: Any = ..., index: Union[ArrayLike, Index, None] = ..., dtype: Union[Dtype, None] = ..., name: Union[str, None] = ..., copy: bool = ..., fastpath: bool = ..., dtype_if_empty: Dtype = ...) -> Series: ...
