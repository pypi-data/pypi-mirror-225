from sklearn.base import BaseEstimator as BaseEstimator

class NoTagsEstimator: ...
class MoreTagsEstimator: ...

def test_safe_tags_error(estimator, err_msg) -> None: ...
def test_safe_tags_no_get_tags(estimator, key, expected_results) -> None: ...
