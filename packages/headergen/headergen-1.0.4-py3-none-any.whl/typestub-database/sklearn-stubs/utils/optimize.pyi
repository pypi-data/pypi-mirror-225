from ..exceptions import ConvergenceWarning as ConvergenceWarning
from .fixes import line_search_wolfe1 as line_search_wolfe1, line_search_wolfe2 as line_search_wolfe2

class _LineSearchError(RuntimeError): ...
