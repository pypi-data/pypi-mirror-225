from tensorflow.python.keras import losses as losses
from tensorflow.python.keras.models import Sequential as Sequential
from tensorflow.python.keras.utils.generic_utils import has_arg as has_arg
from tensorflow.python.keras.utils.np_utils import to_categorical as to_categorical
from tensorflow.python.util.tf_export import keras_export as keras_export
from typing import Any

class BaseWrapper:
    build_fn: Any
    sk_params: Any
    def __init__(self, build_fn: Any | None = ..., **sk_params) -> None: ...
    def check_params(self, params) -> None: ...
    def get_params(self, **params): ...
    def set_params(self, **params): ...
    model: Any
    def fit(self, x, y, **kwargs): ...
    def filter_sk_params(self, fn, override: Any | None = ...): ...

class KerasClassifier(BaseWrapper):
    classes_: Any
    n_classes_: Any
    def fit(self, x, y, **kwargs): ...
    def predict(self, x, **kwargs): ...
    def predict_proba(self, x, **kwargs): ...
    def score(self, x, y, **kwargs): ...

class KerasRegressor(BaseWrapper):
    def predict(self, x, **kwargs): ...
    def score(self, x, y, **kwargs): ...
