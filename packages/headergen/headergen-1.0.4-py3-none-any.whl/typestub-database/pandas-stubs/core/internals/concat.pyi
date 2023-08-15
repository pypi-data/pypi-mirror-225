from pandas import Index as Index
from pandas._libs import NaT as NaT
from pandas._typing import ArrayLike as ArrayLike, DtypeObj as DtypeObj, Manager as Manager, Shape as Shape
from pandas.core.arrays import DatetimeArray as DatetimeArray, ExtensionArray as ExtensionArray
from pandas.core.construction import ensure_wrapped_if_datetimelike as ensure_wrapped_if_datetimelike
from pandas.core.dtypes.cast import ensure_dtype_can_hold_na as ensure_dtype_can_hold_na, find_common_type as find_common_type
from pandas.core.dtypes.common import is_1d_only_ea_dtype as is_1d_only_ea_dtype, is_1d_only_ea_obj as is_1d_only_ea_obj, is_datetime64tz_dtype as is_datetime64tz_dtype, is_dtype_equal as is_dtype_equal
from pandas.core.dtypes.concat import cast_to_common_type as cast_to_common_type, concat_compat as concat_compat
from pandas.core.dtypes.dtypes import ExtensionDtype as ExtensionDtype
from pandas.core.internals.array_manager import ArrayManager as ArrayManager, NullArrayProxy as NullArrayProxy
from pandas.core.internals.blocks import Block as Block, ensure_block_shape as ensure_block_shape, new_block_2d as new_block_2d
from pandas.core.internals.managers import BlockManager as BlockManager
from pandas.util._decorators import cache_readonly as cache_readonly
from typing import Union, Any

def concat_arrays(to_concat: list) -> ArrayLike: ...
def concatenate_managers(mgrs_indexers, axes: list[Index], concat_axis: int, copy: bool) -> Manager: ...

class JoinUnit:
    block: Any
    shape: Any
    def __init__(self, block: Block, shape: Shape) -> None: ...
    def is_na(self) -> bool: ...
    def get_reindexed_values(self, empty_dtype: DtypeObj) -> ArrayLike: ...

def make_na_array(dtype: DtypeObj, shape: Shape) -> ArrayLike: ...
