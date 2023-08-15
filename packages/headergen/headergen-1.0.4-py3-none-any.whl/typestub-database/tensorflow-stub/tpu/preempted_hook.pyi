import threading
from tensorflow.python.distribute.cluster_resolver import tpu_cluster_resolver as tpu_cluster_resolver
from tensorflow.python.training import session_run_hook as session_run_hook

class CloudTPUPreemptedHook(session_run_hook.SessionRunHook):
    def __init__(self, cluster) -> None: ...
    def after_create_session(self, session, coord) -> None: ...
    def end(self, session) -> None: ...

class _TPUPollingThread(threading.Thread):
    daemon: bool
    def __init__(self, cluster, session) -> None: ...
    def stop(self) -> None: ...
    def run(self) -> None: ...
