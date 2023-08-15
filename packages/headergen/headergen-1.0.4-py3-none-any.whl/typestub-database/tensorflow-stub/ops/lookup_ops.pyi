from tensorflow.python.ops.gen_lookup_ops import *
from tensorflow.python.eager import context as context
from tensorflow.python.framework import constant_op as constant_op, dtypes as dtypes, ops as ops, sparse_tensor as sparse_tensor, tensor_shape as tensor_shape, tensor_util as tensor_util
from tensorflow.python.ops import array_ops as array_ops, control_flow_ops as control_flow_ops, gen_lookup_ops as gen_lookup_ops, math_ops as math_ops, string_ops as string_ops
from tensorflow.python.ops.ragged import ragged_tensor as ragged_tensor
from tensorflow.python.saved_model import registration as registration
from tensorflow.python.training.saver import BaseSaverBuilder as BaseSaverBuilder
from tensorflow.python.training.tracking import base as trackable_base, tracking as trackable
from tensorflow.python.util.deprecation import deprecated as deprecated
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def initialize_all_tables(name: str = ...): ...
def tables_initializer(name: str = ...): ...
def check_table_dtypes(table, key_dtype, value_dtype) -> None: ...

class LookupInterface(trackable.TrackableResource):
    def __init__(self, key_dtype, value_dtype) -> None: ...
    @property
    def key_dtype(self): ...
    @property
    def value_dtype(self): ...
    @property
    def name(self): ...
    def size(self, name: Any | None = ...) -> None: ...
    def lookup(self, keys, name: Any | None = ...) -> None: ...
    def __getitem__(self, keys): ...

class InitializableLookupTableBase(LookupInterface):
    def __init__(self, default_value, initializer) -> None: ...
    @property
    def default_value(self): ...
    def size(self, name: Any | None = ...): ...
    def lookup(self, keys, name: Any | None = ...): ...

class InitializableLookupTableBaseV1(InitializableLookupTableBase):
    @property
    def initializer(self): ...

class StaticHashTable(InitializableLookupTableBase):
    def __init__(self, initializer, default_value, name: Any | None = ..., experimental_is_anonymous: bool = ...) -> None: ...
    @property
    def name(self): ...
    def export(self, name: Any | None = ...): ...

class StaticHashTableV1(StaticHashTable):
    def __init__(self, initializer, default_value, name: Any | None = ...) -> None: ...
    @property
    def initializer(self): ...

class HashTable(StaticHashTableV1):
    @property
    def init(self): ...

class TableInitializerBase(trackable_base.Trackable):
    def __init__(self, key_dtype, value_dtype) -> None: ...
    @property
    def key_dtype(self): ...
    @property
    def value_dtype(self): ...
    def initialize(self, table) -> None: ...

class KeyValueTensorInitializer(TableInitializerBase):
    def __init__(self, keys, values, key_dtype: Any | None = ..., value_dtype: Any | None = ..., name: Any | None = ...) -> None: ...
    def initialize(self, table): ...

class TextFileIndex:
    WHOLE_LINE: int
    LINE_NUMBER: int

class TextFileInitializer(TableInitializerBase):
    def __init__(self, filename, key_dtype, key_index, value_dtype, value_index, vocab_size: Any | None = ..., delimiter: str = ..., name: Any | None = ..., value_index_offset: int = ...) -> None: ...
    def initialize(self, table): ...

class TextFileStringTableInitializer(TextFileInitializer):
    def __init__(self, filename, key_column_index=..., value_column_index=..., vocab_size: Any | None = ..., delimiter: str = ..., name: str = ...) -> None: ...

class TextFileIdTableInitializer(TextFileInitializer):
    def __init__(self, filename, key_column_index=..., value_column_index=..., vocab_size: Any | None = ..., delimiter: str = ..., name: str = ..., key_dtype=...) -> None: ...

class HasherSpec: ...

FastHashSpec: Any

class StrongHashSpec(HasherSpec):
    def __new__(cls, key): ...

class IdTableWithHashBuckets(LookupInterface):
    def __init__(self, table, num_oov_buckets, hasher_spec=..., name: Any | None = ..., key_dtype: Any | None = ...) -> None: ...
    @property
    def initializer(self): ...
    @property
    def init(self): ...
    @property
    def resource_handle(self): ...
    @property
    def name(self): ...
    def size(self, name: Any | None = ...): ...
    def lookup(self, keys, name: Any | None = ...): ...

class StaticVocabularyTable(LookupInterface):
    def __init__(self, initializer, num_oov_buckets, lookup_key_dtype: Any | None = ..., name: Any | None = ...) -> None: ...
    @property
    def resource_handle(self): ...
    @property
    def name(self): ...
    def size(self, name: Any | None = ...): ...
    def lookup(self, keys, name: Any | None = ...): ...

class StaticVocabularyTableV1(StaticVocabularyTable):
    @property
    def initializer(self): ...

def index_table_from_file(vocabulary_file: Any | None = ..., num_oov_buckets: int = ..., vocab_size: Any | None = ..., default_value: int = ..., hasher_spec=..., key_dtype=..., name: Any | None = ..., key_column_index=..., value_column_index=..., delimiter: str = ...): ...
def index_table_from_tensor(vocabulary_list, num_oov_buckets: int = ..., default_value: int = ..., hasher_spec=..., dtype=..., name: Any | None = ...): ...
def index_to_string_table_from_file(vocabulary_file, vocab_size: Any | None = ..., default_value: str = ..., name: Any | None = ..., key_column_index=..., value_column_index=..., delimiter: str = ...): ...
def index_to_string_table_from_tensor(vocabulary_list, default_value: str = ..., name: Any | None = ...): ...

class MutableHashTable(LookupInterface):
    def __init__(self, key_dtype, value_dtype, default_value, name: str = ..., checkpoint: bool = ...) -> None: ...
    @property
    def name(self): ...
    def size(self, name: Any | None = ...): ...
    def remove(self, keys, name: Any | None = ...): ...
    def lookup(self, keys, dynamic_default_values: Any | None = ..., name: Any | None = ...): ...
    def insert(self, keys, values, name: Any | None = ...): ...
    def export(self, name: Any | None = ...): ...
    class _Saveable(BaseSaverBuilder.SaveableObject):
        table_name: Any
        def __init__(self, table, name, table_name: Any | None = ...) -> None: ...
        def restore(self, restored_tensors, restored_shapes): ...

class DenseHashTable(LookupInterface):
    def __init__(self, key_dtype, value_dtype, default_value, empty_key, deleted_key, initial_num_buckets: Any | None = ..., name: str = ..., checkpoint: bool = ...) -> None: ...
    @property
    def name(self): ...
    def size(self, name: Any | None = ...): ...
    def lookup(self, keys, name: Any | None = ...): ...
    def insert_or_assign(self, keys, values, name: Any | None = ...): ...
    def insert(self, keys, values, name: Any | None = ...): ...
    def erase(self, keys, name: Any | None = ...): ...
    def remove(self, keys, name: Any | None = ...): ...
    def export(self, name: Any | None = ...): ...
    class _Saveable(BaseSaverBuilder.SaveableObject):
        table_name: Any
        def __init__(self, table, name, table_name: Any | None = ...) -> None: ...
        def restore(self, restored_tensors, restored_shapes): ...
