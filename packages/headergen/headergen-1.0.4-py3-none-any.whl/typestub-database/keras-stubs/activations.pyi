from keras import backend as backend
from keras.layers import advanced_activations as advanced_activations
from keras.utils.generic_utils import deserialize_keras_object as deserialize_keras_object, serialize_keras_object as serialize_keras_object
from typing import Any

def softmax(x, axis: int = ...): ...
def elu(x, alpha: float = ...): ...
def selu(x): ...
def softplus(x): ...
def softsign(x): ...
def swish(x): ...
def relu(x, alpha: float = ..., max_value: Any | None = ..., threshold: float = ...): ...
def gelu(x, approximate: bool = ...): ...
def tanh(x): ...
def sigmoid(x): ...
def exponential(x): ...
def hard_sigmoid(x): ...
def linear(x): ...
def serialize(activation): ...

leaky_relu: Any
log_softmax: Any
relu6: Any
silu: Any

def deserialize(name, custom_objects: Any | None = ...): ...
def get(identifier): ...
