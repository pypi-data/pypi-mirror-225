from statsmodels.stats.base import HolderTuple as HolderTuple
from typing import Any

def test_poisson_2indep(count1, exposure1, count2, exposure2, ratio_null: int = ..., method: str = ..., alternative: str = ..., etest_kwds: Any | None = ...): ...
def etest_poisson_2indep(count1, exposure1, count2, exposure2, ratio_null: int = ..., method: str = ..., alternative: str = ..., ygrid: Any | None = ...): ...
def tost_poisson_2indep(count1, exposure1, count2, exposure2, low, upp, method: str = ...): ...
