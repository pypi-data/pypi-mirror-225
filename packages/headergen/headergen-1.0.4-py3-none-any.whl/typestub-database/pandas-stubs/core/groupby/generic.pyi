from pandas._typing import (
    ArrayLike as ArrayLike,
    Manager as Manager,
    Manager2D as Manager2D,
    SingleManager as SingleManager,
)
from pandas.core import algorithms as algorithms, nanops as nanops
from pandas.core.apply import (
    GroupByApply as GroupByApply,
    maybe_mangle_lambdas as maybe_mangle_lambdas,
    reconstruct_func as reconstruct_func,
    validate_func_kwargs as validate_func_kwargs,
)
from pandas.core.base import SpecificationError as SpecificationError
from pandas.core.construction import (
    create_series_with_explicit_dtype as create_series_with_explicit_dtype,
)
from pandas.core.dtypes.common import (
    ensure_int64 as ensure_int64,
    is_bool as is_bool,
    is_categorical_dtype as is_categorical_dtype,
    is_dict_like as is_dict_like,
    is_integer_dtype as is_integer_dtype,
    is_interval_dtype as is_interval_dtype,
    is_scalar as is_scalar,
)
from pandas.core.dtypes.missing import isna as isna, notna as notna
from pandas.core.frame import DataFrame as DataFrame
from pandas.core.generic import NDFrame as NDFrame
from pandas.core.groupby import base as base
from pandas.core.groupby.groupby import (
    GroupBy as GroupBy,
    warn_dropping_nuisance_columns_deprecated as warn_dropping_nuisance_columns_deprecated,
)
from pandas.core.groupby.grouper import get_grouper as get_grouper
from pandas.core.indexes.api import (
    Index as Index,
    MultiIndex as MultiIndex,
    all_indexes_same as all_indexes_same,
)
from pandas.core.series import Series as Series
from pandas.core.util.numba_ import maybe_use_numba as maybe_use_numba
from pandas.plotting import boxplot_frame_groupby as boxplot_frame_groupby
from pandas.util._decorators import (
    Appender as Appender,
    Substitution as Substitution,
    doc as doc,
)
from pandas.util._exceptions import find_stack_level as find_stack_level
from typing import Union, Any, Callable, Hashable, NamedTuple, Sequence, TypeVar, Union

AggScalar = Union[str, Callable[..., Any]]
ScalarResult = TypeVar("ScalarResult")

class NamedAgg(NamedTuple):
    column: Hashable
    aggfunc: AggScalar

def generate_property(name: str, klass: type[Union[DataFrame, Series]]): ...
def pin_allowlisted_properties(
    klass: type[Union[DataFrame, Series]], allowlist: frozenset[str]
): ...

class SeriesGroupBy(GroupBy[Series]):
    def apply(self, func, *args, **kwargs): ...
    def aggregate(
        self,
        func: Any | None = ...,
        *args,
        engine: Any | None = ...,
        engine_kwargs: Any | None = ...,
        **kwargs
    ): ...
    agg: Any
    def transform(
        self,
        func,
        *args,
        engine: Any | None = ...,
        engine_kwargs: Any | None = ...,
        **kwargs
    ): ...
    def filter(self, func, dropna: bool = ..., *args, **kwargs): ...
    def nunique(self, dropna: bool = ...) -> Series: ...
    def describe(self, **kwargs): ...
    def value_counts(
        self,
        normalize: bool = ...,
        sort: bool = ...,
        ascending: bool = ...,
        bins: Any | None = ...,
        dropna: bool = ...,
    ): ...
    def nlargest(self, n: int = ..., keep: str = ...): ...
    def nsmallest(self, n: int = ..., keep: str = ...): ...

class DataFrameGroupBy(GroupBy[DataFrame]):
    def aggregate(
        self,
        func: Any | None = ...,
        *args,
        engine: Any | None = ...,
        engine_kwargs: Any | None = ...,
        **kwargs
    ) -> DataFrame: ...
    agg: Any
    def transform(
        self,
        func,
        *args,
        engine: Any | None = ...,
        engine_kwargs: Any | None = ...,
        **kwargs
    ) -> DataFrame: ...
    def filter(self, func, dropna: bool = ..., *args, **kwargs): ...
    def __getitem__(self, key) -> Union[DataFrameGroupBy, SeriesGroupBy]: ...
    def nunique(self, dropna: bool = ...) -> DataFrame: ...
    def idxmax(self, axis: int = ..., skipna: bool = ...): ...
    def idxmin(self, axis: int = ..., skipna: bool = ...): ...
    boxplot: Any
    def value_counts(
        self,
        subset: Union[Sequence[Hashable], None] = ...,
        normalize: bool = ...,
        sort: bool = ...,
        ascending: bool = ...,
        dropna: bool = ...,
    ) -> Union[DataFrame, Series]: ...
