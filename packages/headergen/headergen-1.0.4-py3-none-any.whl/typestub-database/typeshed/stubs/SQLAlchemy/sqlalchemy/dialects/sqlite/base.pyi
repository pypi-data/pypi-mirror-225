from _typeshed import Incomplete
from typing import Any

import sqlalchemy.types as sqltypes

from ...engine import default
from ...sql import compiler
from ...types import (
    BLOB as BLOB,
    BOOLEAN as BOOLEAN,
    CHAR as CHAR,
    DECIMAL as DECIMAL,
    FLOAT as FLOAT,
    INTEGER as INTEGER,
    NUMERIC as NUMERIC,
    REAL as REAL,
    SMALLINT as SMALLINT,
    TEXT as TEXT,
    TIMESTAMP as TIMESTAMP,
    VARCHAR as VARCHAR,
)
from .json import JSON as JSON

class _SQliteJson(JSON):
    def result_processor(self, dialect, coltype): ...

class _DateTimeMixin:
    def __init__(self, storage_format: Incomplete | None = None, regexp: Incomplete | None = None, **kw) -> None: ...
    @property
    def format_is_text_affinity(self): ...
    def adapt(self, cls, **kw): ...
    def literal_processor(self, dialect): ...

class DATETIME(_DateTimeMixin, sqltypes.DateTime):
    def __init__(self, *args, **kwargs) -> None: ...
    def bind_processor(self, dialect): ...
    def result_processor(self, dialect, coltype): ...

class DATE(_DateTimeMixin, sqltypes.Date):
    def bind_processor(self, dialect): ...
    def result_processor(self, dialect, coltype): ...

class TIME(_DateTimeMixin, sqltypes.Time):
    def __init__(self, *args, **kwargs) -> None: ...
    def bind_processor(self, dialect): ...
    def result_processor(self, dialect, coltype): ...

colspecs: Any
ischema_names: Any

class SQLiteCompiler(compiler.SQLCompiler):
    extract_map: Any
    def visit_now_func(self, fn, **kw): ...
    def visit_localtimestamp_func(self, func, **kw): ...
    def visit_true(self, expr, **kw): ...
    def visit_false(self, expr, **kw): ...
    def visit_char_length_func(self, fn, **kw): ...
    def visit_cast(self, cast, **kwargs): ...
    def visit_extract(self, extract, **kw): ...
    def limit_clause(self, select, **kw): ...
    def for_update_clause(self, select, **kw): ...
    def visit_is_distinct_from_binary(self, binary, operator, **kw): ...
    def visit_is_not_distinct_from_binary(self, binary, operator, **kw): ...
    def visit_json_getitem_op_binary(self, binary, operator, **kw): ...
    def visit_json_path_getitem_op_binary(self, binary, operator, **kw): ...
    def visit_empty_set_op_expr(self, type_, expand_op): ...
    def visit_empty_set_expr(self, element_types): ...
    def visit_regexp_match_op_binary(self, binary, operator, **kw): ...
    def visit_not_regexp_match_op_binary(self, binary, operator, **kw): ...
    def visit_on_conflict_do_nothing(self, on_conflict, **kw): ...
    def visit_on_conflict_do_update(self, on_conflict, **kw): ...

class SQLiteDDLCompiler(compiler.DDLCompiler):
    def get_column_specification(self, column, **kwargs): ...
    def visit_primary_key_constraint(self, constraint): ...
    def visit_unique_constraint(self, constraint): ...
    def visit_check_constraint(self, constraint): ...
    def visit_column_check_constraint(self, constraint): ...
    def visit_foreign_key_constraint(self, constraint): ...
    def define_constraint_remote_table(self, constraint, table, preparer): ...
    def visit_create_index(self, create, include_schema: bool = False, include_table_schema: bool = True): ...  # type: ignore[override]
    def post_create_table(self, table): ...

class SQLiteTypeCompiler(compiler.GenericTypeCompiler):
    def visit_large_binary(self, type_, **kw): ...
    def visit_DATETIME(self, type_, **kw): ...
    def visit_DATE(self, type_, **kw): ...
    def visit_TIME(self, type_, **kw): ...
    def visit_JSON(self, type_, **kw): ...

class SQLiteIdentifierPreparer(compiler.IdentifierPreparer):
    reserved_words: Any

class SQLiteExecutionContext(default.DefaultExecutionContext): ...

class SQLiteDialect(default.DefaultDialect):
    name: str
    supports_alter: bool
    supports_unicode_statements: bool
    supports_unicode_binds: bool
    supports_default_values: bool
    supports_default_metavalue: bool
    supports_empty_insert: bool
    supports_cast: bool
    supports_multivalues_insert: bool
    tuple_in_values: bool
    supports_statement_cache: bool
    default_paramstyle: str
    statement_compiler: Any
    ddl_compiler: Any
    type_compiler: Any
    preparer: Any
    ischema_names: Any
    colspecs: Any
    isolation_level: Any
    construct_arguments: Any
    native_datetime: Any
    def __init__(
        self,
        isolation_level: Incomplete | None = None,
        native_datetime: bool = False,
        json_serializer: Incomplete | None = None,
        json_deserializer: Incomplete | None = None,
        _json_serializer: Incomplete | None = None,
        _json_deserializer: Incomplete | None = None,
        **kwargs,
    ) -> None: ...
    def set_isolation_level(self, connection, level) -> None: ...
    def get_isolation_level(self, connection): ...
    def on_connect(self): ...
    def get_schema_names(self, connection, **kw): ...
    def get_table_names(self, connection, schema: Incomplete | None = None, **kw): ...
    def get_temp_table_names(self, connection, **kw): ...
    def get_temp_view_names(self, connection, **kw): ...
    def has_table(self, connection, table_name, schema: Incomplete | None = None): ...  # type: ignore[override]
    def get_view_names(self, connection, schema: Incomplete | None = None, **kw): ...
    def get_view_definition(self, connection, view_name, schema: Incomplete | None = None, **kw): ...
    def get_columns(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
    def get_pk_constraint(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
    def get_foreign_keys(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
    def get_unique_constraints(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
    def get_check_constraints(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
    def get_indexes(self, connection, table_name, schema: Incomplete | None = None, **kw): ...
