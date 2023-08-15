from keras.engine import base_preprocessing_layer as base_preprocessing_layer, functional as functional, sequential as sequential
from keras.utils import tf_utils as tf_utils

class PreprocessingStage(sequential.Sequential, base_preprocessing_layer.PreprocessingLayer):
    def adapt(self, data, reset_state: bool = ...): ...

class FunctionalPreprocessingStage(functional.Functional, base_preprocessing_layer.PreprocessingLayer):
    def fit(self, *args, **kwargs) -> None: ...
    def adapt(self, data, reset_state: bool = ...): ...
