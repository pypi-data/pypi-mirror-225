from sklearn.cluster import AgglomerativeClustering as AgglomerativeClustering, Birch as Birch
from sklearn.cluster.tests.common import generate_clustered_data as generate_clustered_data
from sklearn.datasets import make_blobs as make_blobs
from sklearn.exceptions import ConvergenceWarning as ConvergenceWarning
from sklearn.linear_model import ElasticNet as ElasticNet
from sklearn.metrics import pairwise_distances_argmin as pairwise_distances_argmin, v_measure_score as v_measure_score
from sklearn.utils._testing import assert_almost_equal as assert_almost_equal, assert_array_almost_equal as assert_array_almost_equal, assert_array_equal as assert_array_equal

def test_n_samples_leaves_roots() -> None: ...
def test_partial_fit() -> None: ...
def test_birch_predict() -> None: ...
def test_n_clusters() -> None: ...
def test_sparse_X() -> None: ...
def test_partial_fit_second_call_error_checks() -> None: ...
def check_branching_factor(node, branching_factor) -> None: ...
def test_branching_factor() -> None: ...
def check_threshold(birch_instance, threshold) -> None: ...
def test_threshold() -> None: ...
def test_birch_n_clusters_long_int() -> None: ...
def test_birch_fit_attributes_deprecated(attribute) -> None: ...
