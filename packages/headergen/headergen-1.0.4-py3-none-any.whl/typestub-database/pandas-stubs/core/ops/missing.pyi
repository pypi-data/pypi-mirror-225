import numpy as np
from pandas.core.dtypes.common import is_float_dtype as is_float_dtype, is_integer_dtype as is_integer_dtype, is_scalar as is_scalar
from pandas.core.ops import roperator as roperator

def mask_zero_div_zero(x, y, result: np.ndarray) -> np.ndarray: ...
def dispatch_fill_zeros(op, left, right, result): ...
