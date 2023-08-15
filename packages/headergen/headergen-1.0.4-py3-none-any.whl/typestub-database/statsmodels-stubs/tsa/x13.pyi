from typing import Any

class _freq_to_period:
    def __getitem__(self, key): ...

class Spec:
    @property
    def spec_name(self): ...
    def create_spec(self, **kwargs): ...
    options: Any
    def set_options(self, **kwargs) -> None: ...

class SeriesSpec(Spec):
    def __init__(self, data, name: str = ..., appendbcst: bool = ..., appendfcst: bool = ..., comptype: Any | None = ..., compwt: int = ..., decimals: int = ..., modelspan=..., period: int = ..., precision: int = ..., to_print=..., to_save=..., span=..., start=..., title: str = ..., series_type: Any | None = ..., divpower: Any | None = ..., missingcode: int = ..., missingval: int = ...) -> None: ...

def x13_arima_analysis(endog, maxorder=..., maxdiff=..., diff: Any | None = ..., exog: Any | None = ..., log: Any | None = ..., outlier: bool = ..., trading: bool = ..., forecast_periods: Any | None = ..., retspec: bool = ..., speconly: bool = ..., start: Any | None = ..., freq: Any | None = ..., print_stdout: bool = ..., x12path: Any | None = ..., prefer_x13: bool = ...): ...
def x13_arima_select_order(endog, maxorder=..., maxdiff=..., diff: Any | None = ..., exog: Any | None = ..., log: Any | None = ..., outlier: bool = ..., trading: bool = ..., forecast_periods: Any | None = ..., start: Any | None = ..., freq: Any | None = ..., print_stdout: bool = ..., x12path: Any | None = ..., prefer_x13: bool = ...): ...

class X13ArimaAnalysisResult:
    def __init__(self, **kwargs) -> None: ...
    def plot(self): ...
