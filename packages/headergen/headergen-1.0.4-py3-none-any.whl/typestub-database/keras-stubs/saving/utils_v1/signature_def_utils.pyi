from keras.saving.utils_v1 import unexported_constants as unexported_constants
from typing import Any

def supervised_train_signature_def(inputs, loss, predictions: Any | None = ..., metrics: Any | None = ...): ...
def supervised_eval_signature_def(inputs, loss, predictions: Any | None = ..., metrics: Any | None = ...): ...
