from sklearn.ensemble._hist_gradient_boosting._bitset import in_bitset_memoryview as in_bitset_memoryview, set_bitset_memoryview as set_bitset_memoryview, set_raw_bitset_from_binned_bitset as set_raw_bitset_from_binned_bitset
from sklearn.ensemble._hist_gradient_boosting.common import X_DTYPE as X_DTYPE

def test_set_get_bitset(values_to_insert, expected_bitset) -> None: ...
def test_raw_bitset_from_binned_bitset(raw_categories, binned_cat_to_insert, expected_raw_bitset) -> None: ...
