from tensorflow.python.autograph.core import converter as converter
from tensorflow.python.autograph.pyct import anno as anno, parser as parser, qual_names as qual_names, templates as templates
from tensorflow.python.autograph.pyct.static_analysis import activity as activity
from tensorflow.python.autograph.pyct.static_analysis.annos import NodeAnno as NodeAnno
from typing import Any

BODY_DEFINITELY_RETURNS: str
ORELSE_DEFINITELY_RETURNS: str
STMT_DEFINITELY_RETURNS: str

class _RewriteBlock:
    definitely_returns: bool
    def __init__(self) -> None: ...

class ConditionalReturnRewriter(converter.Base):
    def visit_Return(self, node): ...
    def visit_While(self, node): ...
    def visit_For(self, node): ...
    def visit_With(self, node): ...
    def visit_Try(self, node): ...
    def visit_ExceptHandler(self, node): ...
    def visit_If(self, node): ...
    def visit_FunctionDef(self, node): ...

class _Block:
    is_function: bool
    return_used: bool
    create_guard_next: bool
    create_guard_now: bool
    def __init__(self) -> None: ...

class _Function:
    do_return_var_name: Any
    retval_var_name: Any
    def __init__(self) -> None: ...

class ReturnStatementsTransformer(converter.Base):
    allow_missing_return: Any
    def __init__(self, ctx, allow_missing_return) -> None: ...
    def visit_Return(self, node): ...
    def visit_While(self, node): ...
    def visit_For(self, node): ...
    def visit_With(self, node): ...
    def visit_Try(self, node): ...
    def visit_ExceptHandler(self, node): ...
    def visit_If(self, node): ...
    def visit_FunctionDef(self, node): ...

def transform(node, ctx, default_to_null_return: bool = ...): ...
