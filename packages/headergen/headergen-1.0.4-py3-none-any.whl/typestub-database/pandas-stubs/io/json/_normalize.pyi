from pandas import DataFrame as DataFrame
from pandas._libs.writers import convert_json_to_lines as convert_json_to_lines
from pandas._typing import Scalar as Scalar
from pandas.util._decorators import deprecate as deprecate
from typing import Union, Any

def convert_to_line_delimits(s: str) -> str: ...
def nested_to_record(ds, prefix: str = ..., sep: str = ..., level: int = ..., max_level: Union[int, None] = ...): ...

json_normalize: Any
