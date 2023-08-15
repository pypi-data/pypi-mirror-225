import numpy as np
from pandas._libs import lib as lib
from pandas.core.dtypes.generic import ABCDataFrame as ABCDataFrame, ABCSeries as ABCSeries
from pandas.core.generic import NDFrame as NDFrame

def preprocess_weights(obj: NDFrame, weights, axis: int) -> np.ndarray: ...
def process_sampling_size(n: Union[int, None], frac: Union[float, None], replace: bool) -> Union[int, None]: ...
def sample(obj_len: int, size: int, replace: bool, weights: Union[np.ndarray, None], random_state: Union[np.random.RandomState, np.random.Generator]) -> np.ndarray: ...
