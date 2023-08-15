from sklearn.datasets import make_multilabel_classification as make_multilabel_classification
from sklearn.metrics import accuracy_score as accuracy_score, average_precision_score as average_precision_score, balanced_accuracy_score as balanced_accuracy_score, brier_score_loss as brier_score_loss, cohen_kappa_score as cohen_kappa_score, confusion_matrix as confusion_matrix, coverage_error as coverage_error, d2_tweedie_score as d2_tweedie_score, dcg_score as dcg_score, det_curve as det_curve, explained_variance_score as explained_variance_score, f1_score as f1_score, fbeta_score as fbeta_score, hamming_loss as hamming_loss, hinge_loss as hinge_loss, jaccard_score as jaccard_score, label_ranking_average_precision_score as label_ranking_average_precision_score, label_ranking_loss as label_ranking_loss, log_loss as log_loss, matthews_corrcoef as matthews_corrcoef, max_error as max_error, mean_absolute_error as mean_absolute_error, mean_absolute_percentage_error as mean_absolute_percentage_error, mean_gamma_deviance as mean_gamma_deviance, mean_pinball_loss as mean_pinball_loss, mean_poisson_deviance as mean_poisson_deviance, mean_squared_error as mean_squared_error, mean_tweedie_deviance as mean_tweedie_deviance, median_absolute_error as median_absolute_error, multilabel_confusion_matrix as multilabel_confusion_matrix, ndcg_score as ndcg_score, precision_recall_curve as precision_recall_curve, precision_score as precision_score, r2_score as r2_score, recall_score as recall_score, roc_auc_score as roc_auc_score, roc_curve as roc_curve, top_k_accuracy_score as top_k_accuracy_score, zero_one_loss as zero_one_loss
from sklearn.preprocessing import LabelBinarizer as LabelBinarizer
from sklearn.utils import shuffle as shuffle
from sklearn.utils._testing import assert_allclose as assert_allclose, assert_almost_equal as assert_almost_equal, assert_array_equal as assert_array_equal, assert_array_less as assert_array_less, ignore_warnings as ignore_warnings
from sklearn.utils.multiclass import type_of_target as type_of_target
from sklearn.utils.validation import check_random_state as check_random_state
from typing import Any

REGRESSION_METRICS: Any
CLASSIFICATION_METRICS: Any

def precision_recall_curve_padded_thresholds(*args, **kwargs): ...

CURVE_METRICS: Any
THRESHOLDED_METRICS: Any
ALL_METRICS: Any
METRIC_UNDEFINED_BINARY: Any
METRIC_UNDEFINED_MULTICLASS: Any
METRIC_UNDEFINED_BINARY_MULTICLASS: Any
METRICS_WITH_AVERAGING: Any
THRESHOLDED_METRICS_WITH_AVERAGING: Any
METRICS_WITH_POS_LABEL: Any
METRICS_WITH_LABELS: Any
METRICS_WITH_NORMALIZE_OPTION: Any
THRESHOLDED_MULTILABEL_METRICS: Any
MULTILABELS_METRICS: Any
MULTIOUTPUT_METRICS: Any
SYMMETRIC_METRICS: Any
NOT_SYMMETRIC_METRICS: Any
METRICS_WITHOUT_SAMPLE_WEIGHT: Any
METRICS_REQUIRE_POSITIVE_Y: Any

def test_symmetry_consistency() -> None: ...
def test_symmetric_metric(name) -> None: ...
def test_not_symmetric_metric(name) -> None: ...
def test_sample_order_invariance(name) -> None: ...
def test_sample_order_invariance_multilabel_and_multioutput() -> None: ...
def test_format_invariance_with_1d_vectors(name) -> None: ...
def test_classification_invariance_string_vs_numbers_labels(name) -> None: ...
def test_thresholded_invariance_string_vs_numbers_labels(name) -> None: ...

invalids_nan_inf: Any

def test_regression_thresholded_inf_nan_input(metric, y_true, y_score) -> None: ...
def test_classification_inf_nan_input(metric, y_true, y_score) -> None: ...
def test_classification_binary_continuous_input(metric) -> None: ...
def check_single_sample(name) -> None: ...
def check_single_sample_multioutput(name) -> None: ...
def test_single_sample(name) -> None: ...
def test_single_sample_multioutput(name) -> None: ...
def test_multioutput_number_of_output_differ(name) -> None: ...
def test_multioutput_regression_invariance_to_dimension_shuffling(name) -> None: ...
def test_multilabel_representation_invariance() -> None: ...
def test_raise_value_error_multilabel_sequences(name) -> None: ...
def test_normalize_option_binary_classification(name) -> None: ...
def test_normalize_option_multiclass_classification(name) -> None: ...
def test_normalize_option_multilabel_classification(name) -> None: ...
def check_averaging(name, y_true, y_true_binarize, y_pred, y_pred_binarize, y_score) -> None: ...
def test_averaging_multiclass(name) -> None: ...
def test_averaging_multilabel(name) -> None: ...
def test_averaging_multilabel_all_zeroes(name) -> None: ...
def test_averaging_binary_multilabel_all_zeroes(): ...
def test_averaging_multilabel_all_ones(name) -> None: ...
def check_sample_weight_invariance(name, metric, y1, y2) -> None: ...
def test_regression_sample_weight_invariance(name) -> None: ...
def test_binary_sample_weight_invariance(name) -> None: ...
def test_multiclass_sample_weight_invariance(name) -> None: ...
def test_multilabel_sample_weight_invariance(name) -> None: ...
def test_no_averaging_labels() -> None: ...
def test_multilabel_label_permutations_invariance(name) -> None: ...
def test_thresholded_multilabel_multioutput_permutations_invariance(name) -> None: ...
def test_thresholded_metric_permutation_invariance(name) -> None: ...
def test_metrics_consistent_type_error(metric_name) -> None: ...
def test_metrics_pos_label_error_str(metric, y_pred_threshold, dtype_y_str) -> None: ...
