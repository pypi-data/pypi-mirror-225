from typing import Any

def get_current_worker_context(): ...

class _TaskType:
    PS: str
    WORKER: str
    CHIEF: str
    EVALUATOR: str
    CLIENT: str

class _WorkerContext:
    def __init__(self, strategy, cluster_spec, task_type, task_id, session_config: Any | None = ..., rpc_layer: str = ..., worker_barrier: Any | None = ...) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, unused_exception_type, unused_exception_value, unused_traceback) -> None: ...
    def wait_for_other_workers(self) -> None: ...
    def session_creator(self, scaffold: Any | None = ..., config: Any | None = ..., checkpoint_dir: Any | None = ..., checkpoint_filename_with_path: Any | None = ..., max_wait_secs: int = ...): ...
    @property
    def session_config(self): ...
    @property
    def has_barrier(self): ...
    @property
    def distributed_mode(self): ...
    @property
    def cluster_spec(self): ...
    @property
    def task_type(self): ...
    @property
    def task_id(self): ...
    @property
    def master_target(self): ...
    @property
    def is_chief(self): ...
    @property
    def num_workers(self): ...
    @property
    def experimental_should_init(self): ...
    @property
    def should_checkpoint(self): ...
    @property
    def should_save_summary(self): ...

def run_distribute_coordinator(worker_fn, strategy, eval_fn: Any | None = ..., eval_strategy: Any | None = ..., cluster_spec: Any | None = ..., task_type: Any | None = ..., task_id: Any | None = ..., session_config: Any | None = ..., rpc_layer: str = ...): ...
def normalize_cluster_spec(cluster_spec): ...
