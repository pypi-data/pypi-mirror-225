from sklearn.base import BaseEstimator as BaseEstimator, ClassifierMixin as ClassifierMixin, is_classifier as is_classifier
from sklearn.cluster import KMeans as KMeans
from sklearn.datasets import make_blobs as make_blobs, make_classification as make_classification, make_multilabel_classification as make_multilabel_classification
from sklearn.ensemble import HistGradientBoostingClassifier as HistGradientBoostingClassifier
from sklearn.exceptions import NotFittedError as NotFittedError
from sklearn.impute import SimpleImputer as SimpleImputer
from sklearn.linear_model import LinearRegression as LinearRegression, Ridge as Ridge, SGDClassifier as SGDClassifier
from sklearn.metrics import accuracy_score as accuracy_score, confusion_matrix as confusion_matrix, f1_score as f1_score, make_scorer as make_scorer, r2_score as r2_score, recall_score as recall_score, roc_auc_score as roc_auc_score
from sklearn.metrics.pairwise import euclidean_distances as euclidean_distances
from sklearn.model_selection import GridSearchCV as GridSearchCV, GroupKFold as GroupKFold, GroupShuffleSplit as GroupShuffleSplit, KFold as KFold, LeaveOneGroupOut as LeaveOneGroupOut, LeavePGroupsOut as LeavePGroupsOut, ParameterGrid as ParameterGrid, ParameterSampler as ParameterSampler, RandomizedSearchCV as RandomizedSearchCV, StratifiedKFold as StratifiedKFold, StratifiedShuffleSplit as StratifiedShuffleSplit, train_test_split as train_test_split
from sklearn.model_selection._search import BaseSearchCV as BaseSearchCV
from sklearn.model_selection._validation import FitFailedWarning as FitFailedWarning
from sklearn.model_selection.tests.common import OneTimeSplitter as OneTimeSplitter
from sklearn.neighbors import KNeighborsClassifier as KNeighborsClassifier, KernelDensity as KernelDensity, LocalOutlierFactor as LocalOutlierFactor
from sklearn.pipeline import Pipeline as Pipeline
from sklearn.svm import LinearSVC as LinearSVC, SVC as SVC
from sklearn.tree import DecisionTreeClassifier as DecisionTreeClassifier, DecisionTreeRegressor as DecisionTreeRegressor
from sklearn.utils._mocking import CheckingClassifier as CheckingClassifier, MockDataFrame as MockDataFrame
from sklearn.utils._testing import MinimalClassifier as MinimalClassifier, MinimalRegressor as MinimalRegressor, MinimalTransformer as MinimalTransformer, assert_allclose as assert_allclose, assert_almost_equal as assert_almost_equal, assert_array_almost_equal as assert_array_almost_equal, assert_array_equal as assert_array_equal, ignore_warnings as ignore_warnings
from typing import Any

class MockClassifier:
    foo_param: Any
    def __init__(self, foo_param: int = ...) -> None: ...
    classes_: Any
    def fit(self, X, Y): ...
    def predict(self, T): ...
    def transform(self, X): ...
    def inverse_transform(self, X): ...
    predict_proba: Any
    predict_log_proba: Any
    decision_function: Any
    def score(self, X: Any | None = ..., Y: Any | None = ...): ...
    def get_params(self, deep: bool = ...): ...
    def set_params(self, **params): ...

class LinearSVCNoScore(LinearSVC):
    @property
    def score(self) -> None: ...

X: Any
y: Any

def assert_grid_iter_equals_getitem(grid) -> None: ...
def test_validate_parameter_input(klass, input, error_type, error_message) -> None: ...
def test_parameter_grid() -> None: ...
def test_grid_search() -> None: ...
def test_grid_search_pipeline_steps() -> None: ...
def test_SearchCV_with_fit_params(SearchCV) -> None: ...
def test_grid_search_no_score() -> None: ...
def test_grid_search_score_method() -> None: ...
def test_grid_search_groups() -> None: ...
def test_classes__property() -> None: ...
def test_trivial_cv_results_attr() -> None: ...
def test_no_refit() -> None: ...
def test_grid_search_error() -> None: ...
def test_grid_search_one_grid_point() -> None: ...
def test_grid_search_when_param_grid_includes_range() -> None: ...
def test_grid_search_bad_param_grid() -> None: ...
def test_grid_search_sparse() -> None: ...
def test_grid_search_sparse_scoring(): ...
def test_grid_search_precomputed_kernel() -> None: ...
def test_grid_search_precomputed_kernel_error_nonsquare() -> None: ...

class BrokenClassifier(BaseEstimator):
    parameter: Any
    def __init__(self, parameter: Any | None = ...) -> None: ...
    has_been_fit_: bool
    def fit(self, X, y) -> None: ...
    def predict(self, X): ...

def test_refit() -> None: ...
def test_refit_callable(): ...
def test_refit_callable_invalid_type() -> None: ...
def test_refit_callable_out_bound(out_bound_value, search_cv): ...
def test_refit_callable_multi_metric(): ...
def test_gridsearch_nd(): ...
def test_X_as_list(): ...
def test_y_as_list(): ...
def test_pandas_input(): ...
def test_unsupervised_grid_search() -> None: ...
def test_gridsearch_no_predict(): ...
def test_param_sampler() -> None: ...
def check_cv_results_array_types(search, param_keys, score_keys) -> None: ...
def check_cv_results_keys(cv_results, param_keys, score_keys, n_cand) -> None: ...
def test_grid_search_cv_results() -> None: ...
def test_random_search_cv_results() -> None: ...
def test_search_default_iid(SearchCV, specialized_params) -> None: ...
def test_grid_search_cv_results_multimetric() -> None: ...
def test_random_search_cv_results_multimetric() -> None: ...
def compare_cv_results_multimetric_with_single(search_multi, search_acc, search_rec) -> None: ...
def compare_refit_methods_when_refit_with_acc(search_multi, search_acc, refit) -> None: ...
def test_search_cv_score_samples_error(search_cv) -> None: ...
def test_search_cv_score_samples_method(search_cv) -> None: ...
def test_search_cv_results_rank_tie_breaking() -> None: ...
def test_search_cv_results_none_param() -> None: ...
def test_search_cv_timing() -> None: ...
def test_grid_search_correct_score_results() -> None: ...
def test_pickle() -> None: ...
def test_grid_search_with_multioutput_data() -> None: ...
def test_predict_proba_disabled() -> None: ...
def test_grid_search_allows_nans() -> None: ...

class FailingClassifier(BaseEstimator):
    FAILING_PARAMETER: int
    parameter: Any
    def __init__(self, parameter: Any | None = ...) -> None: ...
    def fit(self, X, y: Any | None = ...) -> None: ...
    def predict(self, X): ...
    def score(self, X: Any | None = ..., Y: Any | None = ...): ...

def test_grid_search_failing_classifier(): ...
def test_grid_search_failing_classifier_raise() -> None: ...
def test_parameters_sampler_replacement() -> None: ...
def test_stochastic_gradient_loss_param() -> None: ...
def test_search_train_scores_set_to_false() -> None: ...
def test_grid_search_cv_splits_consistency(): ...
def test_transform_inverse_transform_round_trip() -> None: ...
def test_custom_run_search(): ...
def test__custom_fit_no_run_search(): ...
def test_empty_cv_iterator_error() -> None: ...
def test_random_search_bad_cv(): ...
def test_searchcv_raise_warning_with_non_finite_score(SearchCV, specialized_params, return_train_score): ...
def test_callable_multimetric_confusion_matrix(): ...
def test_callable_multimetric_same_as_list_of_strings(): ...
def test_callable_single_metric_same_as_single_string(): ...
def test_callable_multimetric_error_on_invalid_key(): ...
def test_callable_multimetric_error_failing_clf(): ...
def test_callable_multimetric_clf_all_fails(): ...
def test_n_features_in() -> None: ...
def test_search_cv_pairwise_property_delegated_to_base_estimator(pairwise): ...
def test_search_cv__pairwise_property_delegated_to_base_estimator() -> None: ...
def test_search_cv_pairwise_property_equivalence_of_precomputed() -> None: ...
def test_scalar_fit_param(SearchCV, param_search): ...
def test_scalar_fit_param_compat(SearchCV, param_search): ...
def test_search_cv_using_minimal_compatible_estimator(SearchCV, Predictor) -> None: ...
def test_search_cv_verbose_3(capsys, return_train_score) -> None: ...
