import numpy as np
from pandas._libs import lib as lib
from pandas._libs.arrays import NDArrayBacked as NDArrayBacked
from pandas._typing import ArrayLike as ArrayLike, Dtype as Dtype, F as F, NumpySorter as NumpySorter, NumpyValueArrayLike as NumpyValueArrayLike, PositionalIndexer2D as PositionalIndexer2D, PositionalIndexerTuple as PositionalIndexerTuple, ScalarIndexer as ScalarIndexer, SequenceIndexer as SequenceIndexer, Shape as Shape, TakeIndexer as TakeIndexer, npt as npt, type_t as type_t
from pandas.core import missing as missing
from pandas.core.algorithms import take as take, unique as unique, value_counts as value_counts
from pandas.core.array_algos.quantile import quantile_with_mask as quantile_with_mask
from pandas.core.array_algos.transforms import shift as shift
from pandas.core.arrays.base import ExtensionArray as ExtensionArray
from pandas.core.construction import extract_array as extract_array
from pandas.core.dtypes.common import is_dtype_equal as is_dtype_equal, pandas_dtype as pandas_dtype
from pandas.core.dtypes.dtypes import DatetimeTZDtype as DatetimeTZDtype, ExtensionDtype as ExtensionDtype, PeriodDtype as PeriodDtype
from pandas.core.dtypes.missing import array_equivalent as array_equivalent
from pandas.core.indexers import check_array_indexer as check_array_indexer
from pandas.core.sorting import nargminmax as nargminmax
from pandas.errors import AbstractMethodError as AbstractMethodError
from pandas.util._decorators import doc as doc
from pandas.util._validators import validate_bool_kwarg as validate_bool_kwarg, validate_fillna_kwargs as validate_fillna_kwargs, validate_insert_loc as validate_insert_loc
from typing import Union, Any, Literal, TypeVar, overload

NDArrayBackedExtensionArrayT = TypeVar('NDArrayBackedExtensionArrayT', bound='NDArrayBackedExtensionArray')

def ravel_compat(meth: F) -> F: ...

class NDArrayBackedExtensionArray(NDArrayBacked, ExtensionArray):
    def view(self, dtype: Union[Dtype, None] = ...) -> ArrayLike: ...
    def take(self, indices: TakeIndexer, *, allow_fill: bool = ..., fill_value: Any = ..., axis: int = ...) -> NDArrayBackedExtensionArrayT: ...
    def equals(self, other) -> bool: ...
    def argmin(self, axis: int = ..., skipna: bool = ...): ...
    def argmax(self, axis: int = ..., skipna: bool = ...): ...
    def unique(self) -> NDArrayBackedExtensionArrayT: ...
    def searchsorted(self, value: Union[NumpyValueArrayLike, ExtensionArray], side: Literal[left, right] = ..., sorter: NumpySorter = ...) -> Union[npt.NDArray[np.intp], np.intp]: ...
    def shift(self, periods: int = ..., fill_value: Any | None = ..., axis: int = ...): ...
    def __setitem__(self, key, value) -> None: ...
    @overload
    def __getitem__(self, key: ScalarIndexer) -> Any: ...
    @overload
    def __getitem__(self, key: Union[SequenceIndexer, PositionalIndexerTuple]) -> NDArrayBackedExtensionArrayT: ...
    def fillna(self, value: Any | None = ..., method: Any | None = ..., limit: Any | None = ...) -> NDArrayBackedExtensionArrayT: ...
    def insert(self, loc: int, item) -> NDArrayBackedExtensionArrayT: ...
    def value_counts(self, dropna: bool = ...): ...
