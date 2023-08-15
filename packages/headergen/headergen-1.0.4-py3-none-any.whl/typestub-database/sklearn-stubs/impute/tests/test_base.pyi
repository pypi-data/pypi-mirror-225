from sklearn.impute._base import _BaseImputer
from typing import Any

def data(): ...

class NoFitIndicatorImputer(_BaseImputer):
    def fit(self, X, y: Any | None = ...): ...
    def transform(self, X, y: Any | None = ...): ...

class NoTransformIndicatorImputer(_BaseImputer):
    def fit(self, X, y: Any | None = ...): ...
    def transform(self, X, y: Any | None = ...): ...

class NoPrecomputedMaskFit(_BaseImputer):
    def fit(self, X, y: Any | None = ...): ...
    def transform(self, X): ...

class NoPrecomputedMaskTransform(_BaseImputer):
    def fit(self, X, y: Any | None = ...): ...
    def transform(self, X): ...

def test_base_imputer_not_fit(data) -> None: ...
def test_base_imputer_not_transform(data) -> None: ...
def test_base_no_precomputed_mask_fit(data) -> None: ...
def test_base_no_precomputed_mask_transform(data) -> None: ...
