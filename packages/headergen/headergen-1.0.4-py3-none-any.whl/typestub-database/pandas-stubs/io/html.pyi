from pandas._typing import FilePath as FilePath, ReadBuffer as ReadBuffer
from pandas.compat._optional import import_optional_dependency as import_optional_dependency
from pandas.core.construction import create_series_with_explicit_dtype as create_series_with_explicit_dtype
from pandas.core.dtypes.common import is_list_like as is_list_like
from pandas.core.frame import DataFrame as DataFrame
from pandas.errors import AbstractMethodError as AbstractMethodError, EmptyDataError as EmptyDataError
from pandas.io.common import file_exists as file_exists, get_handle as get_handle, is_url as is_url, stringify_path as stringify_path, urlopen as urlopen, validate_header_arg as validate_header_arg
from pandas.io.formats.printing import pprint_thing as pprint_thing
from pandas.io.parsers import TextParser as TextParser
from pandas.util._decorators import deprecate_nonkeyword_arguments as deprecate_nonkeyword_arguments
from typing import Union, Any, Pattern, Sequence

class _HtmlFrameParser:
    io: Any
    match: Any
    attrs: Any
    encoding: Any
    displayed_only: Any
    def __init__(self, io: Union[FilePath, ReadBuffer[str], ReadBuffer[bytes]], match: Union[str, Pattern], attrs: Union[dict[str, str], None], encoding: str, displayed_only: bool) -> None: ...
    def parse_tables(self): ...

class _BeautifulSoupHtml5LibFrameParser(_HtmlFrameParser):
    def __init__(self, *args, **kwargs) -> None: ...

class _LxmlFrameParser(_HtmlFrameParser): ...

def read_html(io: Union[FilePath, ReadBuffer[str]], match: Union[str, Pattern] = ..., flavor: Union[str, None] = ..., header: Union[int, Sequence[int], None] = ..., index_col: Union[int, Sequence[int], None] = ..., skiprows: Union[int, Sequence[int], slice, None] = ..., attrs: Union[dict[str, str], None] = ..., parse_dates: bool = ..., thousands: Union[str, None] = ..., encoding: Union[str, None] = ..., decimal: str = ..., converters: Union[dict, None] = ..., na_values: Any | None = ..., keep_default_na: bool = ..., displayed_only: bool = ...) -> list[DataFrame]: ...
