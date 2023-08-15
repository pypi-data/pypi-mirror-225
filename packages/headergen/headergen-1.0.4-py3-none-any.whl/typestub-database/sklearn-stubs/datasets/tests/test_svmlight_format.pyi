from sklearn.datasets import dump_svmlight_file as dump_svmlight_file, load_svmlight_file as load_svmlight_file, load_svmlight_files as load_svmlight_files
from sklearn.utils._testing import assert_array_almost_equal as assert_array_almost_equal, assert_array_equal as assert_array_equal, fails_if_pypy as fails_if_pypy

TEST_DATA_MODULE: str
datafile: str
multifile: str
invalidfile: str
invalidfile2: str
pytestmark = fails_if_pypy

def test_load_svmlight_file() -> None: ...
def test_load_svmlight_file_fd() -> None: ...
def test_load_svmlight_file_multilabel() -> None: ...
def test_load_svmlight_files() -> None: ...
def test_load_svmlight_file_n_features() -> None: ...
def test_load_compressed() -> None: ...
def test_load_invalid_file() -> None: ...
def test_load_invalid_order_file() -> None: ...
def test_load_zero_based() -> None: ...
def test_load_zero_based_auto() -> None: ...
def test_load_with_qid() -> None: ...
def test_load_large_qid() -> None: ...
def test_load_invalid_file2() -> None: ...
def test_not_a_filename() -> None: ...
def test_invalid_filename() -> None: ...
def test_dump() -> None: ...
def test_dump_multilabel() -> None: ...
def test_dump_concise() -> None: ...
def test_dump_comment() -> None: ...
def test_dump_invalid() -> None: ...
def test_dump_query_id() -> None: ...
def test_load_with_long_qid() -> None: ...
def test_load_zeros() -> None: ...
def test_load_with_offsets(sparsity, n_samples, n_features) -> None: ...
def test_load_offset_exhaustive_splits() -> None: ...
def test_load_with_offsets_error() -> None: ...
