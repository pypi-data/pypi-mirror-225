from statsmodels.discrete.discrete_model import Poisson as Poisson
from statsmodels.regression.linear_model import OLS as OLS
from typing import Any

def plot_probs(freq, probs_predicted, label: str = ..., upp_xlim: Any | None = ..., fig: Any | None = ...): ...
def test_chisquare_prob(results, probs, bin_edges: Any | None = ..., method: Any | None = ...): ...
def test_poisson_zeroinflation(results_poisson, exog_infl: Any | None = ...): ...
def test_poisson_zeroinflation_brock(results_poisson): ...
