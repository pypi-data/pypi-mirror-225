from pandas import DataFrame as DataFrame, Index as Index, IndexSlice as IndexSlice, MultiIndex as MultiIndex, Series as Series, isna as isna
from pandas._config import get_option as get_option
from pandas._libs import lib as lib
from pandas._typing import Level as Level
from pandas.api.types import is_list_like as is_list_like
from pandas.compat._optional import import_optional_dependency as import_optional_dependency
from pandas.core.dtypes.generic import ABCSeries as ABCSeries
from typing import Union, Any, Callable, Dict, List, Optional, Sequence, Tuple, TypedDict, Union

jinja2: Any
BaseFormatter = Union[str, Callable]
ExtFormatter = Union[BaseFormatter, Dict[Any, Optional[BaseFormatter]]]
CSSPair = Tuple[str, Union[str, int, float]]
CSSList = List[CSSPair]
CSSProperties = Union[str, CSSList]

class CSSDict(TypedDict):
    selector: str
    props: CSSProperties
CSSStyles = List[CSSDict]
Subset = Union[slice, Sequence, Index]

class StylerRenderer:
    loader: Any
    env: Any
    template_html: Any
    template_html_table: Any
    template_html_style: Any
    template_latex: Any
    data: Any
    index: Any
    columns: Any
    uuid: Any
    uuid_len: Any
    table_styles: Any
    table_attributes: Any
    caption: Any
    cell_ids: Any
    css: Any
    hide_index_names: bool
    hide_column_names: bool
    hide_index_: Any
    hide_columns_: Any
    hidden_rows: Any
    hidden_columns: Any
    ctx: Any
    ctx_index: Any
    ctx_columns: Any
    cell_context: Any
    tooltips: Any
    def __init__(self, data: Union[DataFrame, Series], uuid: Union[str, None] = ..., uuid_len: int = ..., table_styles: Union[CSSStyles, None] = ..., table_attributes: Union[str, None] = ..., caption: Union[str, tuple, None] = ..., cell_ids: bool = ..., precision: Union[int, None] = ...): ...
    def format(self, formatter: Union[ExtFormatter, None] = ..., subset: Union[Subset, None] = ..., na_rep: Union[str, None] = ..., precision: Union[int, None] = ..., decimal: str = ..., thousands: Union[str, None] = ..., escape: Union[str, None] = ..., hyperlinks: Union[str, None] = ...) -> StylerRenderer: ...
    def format_index(self, formatter: Union[ExtFormatter, None] = ..., axis: Union[int, str] = ..., level: Union[Level, list[Level], None] = ..., na_rep: Union[str, None] = ..., precision: Union[int, None] = ..., decimal: str = ..., thousands: Union[str, None] = ..., escape: Union[str, None] = ..., hyperlinks: Union[str, None] = ...) -> StylerRenderer: ...

def format_table_styles(styles: CSSStyles) -> CSSStyles: ...
def non_reducing_slice(slice_: Subset): ...
def maybe_convert_css_to_tuples(style: CSSProperties) -> CSSList: ...
def refactor_levels(level: Union[Level, list[Level], None], obj: Index) -> list[int]: ...

class Tooltips:
    class_name: Any
    class_properties: Any
    tt_data: Any
    table_styles: Any
    def __init__(self, css_props: CSSProperties = ..., css_name: str = ..., tooltips: DataFrame = ...) -> None: ...
