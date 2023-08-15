from statsmodels.iolib.summary import Summary as Summary
from statsmodels.iolib.table import SimpleTable as SimpleTable
from statsmodels.iolib.tableformatting import fmt_params as fmt_params
from typing import Any

class NewsResults:
    model: Any
    updated: Any
    previous: Any
    news_results: Any
    row_labels: Any
    params: Any
    post_impacted_forecasts: Any
    prev_impacted_forecasts: Any
    update_impacts: Any
    revision_impacts: Any
    total_impacts: Any
    revisions_iloc: Any
    revisions_ix: Any
    updates_iloc: Any
    updates_ix: Any
    news: Any
    update_forecasts: Any
    update_realized: Any
    weights: Any
    def __init__(self, news_results, model, updated, previous, impacted_variable: Any | None = ..., tolerance: float = ..., row_labels: Any | None = ...) -> None: ...
    @property
    def impacted_variable(self): ...
    @impacted_variable.setter
    def impacted_variable(self, value) -> None: ...
    @property
    def tolerance(self): ...
    @tolerance.setter
    def tolerance(self, value) -> None: ...
    @property
    def data_revisions(self): ...
    @property
    def data_updates(self): ...
    @property
    def details_by_impact(self): ...
    @property
    def details_by_update(self): ...
    @property
    def impacts(self): ...
    def summary_impacts(self, impact_date: Any | None = ..., impacted_variable: Any | None = ..., groupby: str = ..., show_revisions_columns: Any | None = ..., sparsify: bool = ..., float_format: str = ...): ...
    def summary_details(self, impact_date: Any | None = ..., impacted_variable: Any | None = ..., update_date: Any | None = ..., updated_variable: Any | None = ..., groupby: str = ..., sparsify: bool = ..., float_format: str = ..., multiple_tables: bool = ...): ...
    def summary_revisions(self, sparsify: bool = ...): ...
    def summary_news(self, sparsify: bool = ...): ...
    def summary(self, impact_date: Any | None = ..., impacted_variable: Any | None = ..., update_date: Any | None = ..., updated_variable: Any | None = ..., impacts_groupby: str = ..., details_groupby: str = ..., show_revisions_columns: Any | None = ..., sparsify: bool = ..., include_details_tables: Any | None = ..., include_revisions_tables: bool = ..., float_format: str = ...): ...
