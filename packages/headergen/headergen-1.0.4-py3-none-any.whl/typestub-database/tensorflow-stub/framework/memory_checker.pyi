from tensorflow.python.profiler.traceme import TraceMe as TraceMe, traceme_wrapper as traceme_wrapper
from tensorflow.python.util import tf_inspect as tf_inspect
from typing import Any

class MemoryChecker:
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback) -> None: ...
    def record_snapshot(self) -> None: ...
    def report(self) -> None: ...
    def assert_no_leak_if_all_possibly_except_one(self) -> None: ...
    def assert_no_new_python_objects(self, threshold: Any | None = ...) -> None: ...
