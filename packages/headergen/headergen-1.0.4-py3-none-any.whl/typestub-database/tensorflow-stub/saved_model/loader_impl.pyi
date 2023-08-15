from tensorflow.core.protobuf import graph_debug_info_pb2 as graph_debug_info_pb2, meta_graph_pb2 as meta_graph_pb2, saved_model_pb2 as saved_model_pb2
from tensorflow.python.framework import ops as ops
from tensorflow.python.lib.io import file_io as file_io
from tensorflow.python.ops import variables as variables
from tensorflow.python.platform import tf_logging as tf_logging
from tensorflow.python.saved_model import constants as constants, signature_def_utils as signature_def_utils
from tensorflow.python.saved_model.pywrap_saved_model import metrics as metrics
from tensorflow.python.util import compat as compat, deprecation as deprecation
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

def parse_saved_model_with_debug_info(export_dir): ...
def parse_saved_model(export_dir): ...
def get_asset_tensors(export_dir, meta_graph_def_to_load, import_scope: Any | None = ...): ...
def get_init_op(meta_graph_def, import_scope: Any | None = ...): ...
def get_train_op(meta_graph_def, import_scope: Any | None = ...): ...
def maybe_saved_model_directory(export_dir): ...
def contains_saved_model(export_dir): ...
def load(sess, tags, export_dir, import_scope: Any | None = ..., **saver_kwargs): ...

class SavedModelLoader:
    def __init__(self, export_dir) -> None: ...
    @property
    def export_dir(self): ...
    @property
    def variables_path(self): ...
    @property
    def saved_model(self): ...
    def get_meta_graph_def_from_tags(self, tags): ...
    def load_graph(self, graph, tags, import_scope: Any | None = ..., **saver_kwargs): ...
    def restore_variables(self, sess, saver, import_scope: Any | None = ...) -> None: ...
    def run_init_ops(self, sess, tags, import_scope: Any | None = ...) -> None: ...
    def load(self, sess, tags, import_scope: Any | None = ..., **saver_kwargs): ...
