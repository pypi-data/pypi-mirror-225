import tensorflow.compat.v2 as tf
from keras.feature_column import dense_features as dense_features
from keras.utils import tf_contextlib as tf_contextlib
from typing import Any

class DenseFeatures(dense_features.DenseFeatures):
    def __init__(self, feature_columns, trainable: bool = ..., name: Any | None = ..., **kwargs) -> None: ...
    def build(self, _) -> None: ...

class _StateManagerImplV2(tf.__internal__.feature_column.StateManager):
    def create_variable(self, feature_column, name, shape, dtype: Any | None = ..., trainable: bool = ..., use_resource: bool = ..., initializer: Any | None = ...): ...

def no_manual_dependency_tracking_scope(obj) -> None: ...
