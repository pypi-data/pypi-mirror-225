from keras import backend as backend, optimizer_v1 as optimizer_v1
from keras.saving import saving_utils as saving_utils
from keras.saving.saved_model import json_utils as json_utils
from keras.utils.generic_utils import LazyLoader as LazyLoader
from keras.utils.io_utils import ask_to_proceed_with_overwrite as ask_to_proceed_with_overwrite
from typing import Any

HDF5_OBJECT_HEADER_LIMIT: int
sequential_lib: Any

def save_model_to_hdf5(model, filepath, overwrite: bool = ..., include_optimizer: bool = ...) -> None: ...
def load_model_from_hdf5(filepath, custom_objects: Any | None = ..., compile: bool = ...): ...
def preprocess_weights_for_loading(layer, weights, original_keras_version: Any | None = ..., original_backend: Any | None = ...): ...
def save_optimizer_weights_to_hdf5_group(hdf5_group, optimizer) -> None: ...
def load_optimizer_weights_from_hdf5_group(hdf5_group): ...
def save_subset_weights_to_hdf5_group(f, weights) -> None: ...
def save_weights_to_hdf5_group(f, model): ...
def load_subset_weights_from_hdf5_group(f): ...
def load_weights_from_hdf5_group(f, model) -> None: ...
def load_weights_from_hdf5_group_by_name(f, model, skip_mismatch: bool = ...) -> None: ...
def save_attributes_to_hdf5_group(group, name, data) -> None: ...
def load_attributes_from_hdf5_group(group, name): ...
