from ..base import TransformerMixin as TransformerMixin
from ..utils import check_array as check_array, safe_mask as safe_mask, safe_sqr as safe_sqr
from abc import ABCMeta
from typing import Any

class SelectorMixin(TransformerMixin, metaclass=ABCMeta):
    def get_support(self, indices: bool = ...): ...
    def transform(self, X): ...
    def inverse_transform(self, X): ...
    def get_feature_names_out(self, input_features: Any | None = ...): ...
