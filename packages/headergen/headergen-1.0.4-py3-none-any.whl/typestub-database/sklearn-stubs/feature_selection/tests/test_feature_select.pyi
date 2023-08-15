from sklearn.datasets import make_classification as make_classification, make_regression as make_regression
from sklearn.feature_selection import GenericUnivariateSelect as GenericUnivariateSelect, SelectFdr as SelectFdr, SelectFpr as SelectFpr, SelectFwe as SelectFwe, SelectKBest as SelectKBest, SelectPercentile as SelectPercentile, chi2 as chi2, f_classif as f_classif, f_oneway as f_oneway, f_regression as f_regression, mutual_info_classif as mutual_info_classif, mutual_info_regression as mutual_info_regression, r_regression as r_regression
from sklearn.utils import safe_mask as safe_mask
from sklearn.utils._testing import assert_almost_equal as assert_almost_equal, assert_array_almost_equal as assert_array_almost_equal, assert_array_equal as assert_array_equal, ignore_warnings as ignore_warnings

def test_f_oneway_vs_scipy_stats() -> None: ...
def test_f_oneway_ints() -> None: ...
def test_f_classif() -> None: ...
def test_r_regression(center) -> None: ...
def test_f_regression() -> None: ...
def test_f_regression_input_dtype() -> None: ...
def test_f_regression_center() -> None: ...
def test_f_classif_multi_class() -> None: ...
def test_select_percentile_classif() -> None: ...
def test_select_percentile_classif_sparse() -> None: ...
def test_select_kbest_classif() -> None: ...
def test_select_kbest_all() -> None: ...
def test_select_kbest_zero() -> None: ...
def test_select_heuristics_classif() -> None: ...
def assert_best_scores_kept(score_filter) -> None: ...
def test_select_percentile_regression() -> None: ...
def test_select_percentile_regression_full() -> None: ...
def test_invalid_percentile() -> None: ...
def test_select_kbest_regression() -> None: ...
def test_select_heuristics_regression() -> None: ...
def test_boundary_case_ch2() -> None: ...
def test_select_fdr_regression(alpha, n_informative): ...
def test_select_fwe_regression() -> None: ...
def test_selectkbest_tiebreaking(): ...
def test_selectpercentile_tiebreaking(): ...
def test_tied_pvalues() -> None: ...
def test_scorefunc_multilabel() -> None: ...
def test_tied_scores() -> None: ...
def test_nans() -> None: ...
def test_score_func_error() -> None: ...
def test_invalid_k() -> None: ...
def test_f_classif_constant_feature() -> None: ...
def test_no_feature_selected() -> None: ...
def test_mutual_info_classif() -> None: ...
def test_mutual_info_regression() -> None: ...
