from sklearn import base as base, datasets as datasets, linear_model as linear_model, svm as svm
from sklearn.datasets import load_digits as load_digits, make_blobs as make_blobs, make_classification as make_classification
from sklearn.exceptions import ConvergenceWarning as ConvergenceWarning
from sklearn.svm.tests import test_svm as test_svm
from sklearn.utils._testing import ignore_warnings as ignore_warnings, skip_if_32bit as skip_if_32bit
from sklearn.utils.extmath import safe_sparse_dot as safe_sparse_dot
from typing import Any

X: Any
X_sp: Any
Y: Any
T: Any
true_result: Any
X2: Any
X2_sp: Any
Y2: Any
T2: Any
true_result2: Any
iris: Any
rng: Any
perm: Any

def check_svm_model_equal(dense_svm, sparse_svm, X_train, y_train, X_test) -> None: ...
def test_svc() -> None: ...
def test_unsorted_indices(): ...
def test_svc_with_custom_kernel(): ...
def test_svc_iris() -> None: ...
def test_sparse_decision_function() -> None: ...
def test_error() -> None: ...
def test_linearsvc() -> None: ...
def test_linearsvc_iris() -> None: ...
def test_weight() -> None: ...
def test_sample_weights() -> None: ...
def test_sparse_liblinear_intercept_handling() -> None: ...
def test_sparse_oneclasssvm(datasets_index, kernel) -> None: ...
def test_sparse_realdata() -> None: ...
def test_sparse_svc_clone_with_callable_kernel(): ...
def test_timeout(): ...
def test_consistent_proba() -> None: ...
