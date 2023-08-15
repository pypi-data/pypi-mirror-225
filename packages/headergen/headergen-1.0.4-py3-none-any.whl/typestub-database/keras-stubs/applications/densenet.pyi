from keras import backend as backend
from keras.applications import imagenet_utils as imagenet_utils
from keras.engine import training as training
from keras.layers import VersionAwareLayers as VersionAwareLayers
from keras.utils import data_utils as data_utils, layer_utils as layer_utils
from typing import Any

BASE_WEIGHTS_PATH: str
DENSENET121_WEIGHT_PATH: Any
DENSENET121_WEIGHT_PATH_NO_TOP: Any
DENSENET169_WEIGHT_PATH: Any
DENSENET169_WEIGHT_PATH_NO_TOP: Any
DENSENET201_WEIGHT_PATH: Any
DENSENET201_WEIGHT_PATH_NO_TOP: Any
layers: Any

def dense_block(x, blocks, name): ...
def transition_block(x, reduction, name): ...
def conv_block(x, growth_rate, name): ...
def DenseNet(blocks, include_top: bool = ..., weights: str = ..., input_tensor: Any | None = ..., input_shape: Any | None = ..., pooling: Any | None = ..., classes: int = ..., classifier_activation: str = ...): ...
def DenseNet121(include_top: bool = ..., weights: str = ..., input_tensor: Any | None = ..., input_shape: Any | None = ..., pooling: Any | None = ..., classes: int = ...): ...
def DenseNet169(include_top: bool = ..., weights: str = ..., input_tensor: Any | None = ..., input_shape: Any | None = ..., pooling: Any | None = ..., classes: int = ...): ...
def DenseNet201(include_top: bool = ..., weights: str = ..., input_tensor: Any | None = ..., input_shape: Any | None = ..., pooling: Any | None = ..., classes: int = ...): ...
def preprocess_input(x, data_format: Any | None = ...): ...
def decode_predictions(preds, top: int = ...): ...

DOC: str
