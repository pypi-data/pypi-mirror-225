from tensorflow.core.framework.summary_pb2 import Summary as Summary
from tensorflow.core.protobuf import config_pb2 as config_pb2
from tensorflow.core.util.event_pb2 import SessionLog as SessionLog
from tensorflow.python.client import timeline as timeline
from tensorflow.python.framework import dtypes as dtypes, errors as errors, meta_graph as meta_graph, ops as ops
from tensorflow.python.ops import init_ops as init_ops, variable_scope as variable_scope
from tensorflow.python.platform import gfile as gfile
from tensorflow.python.training import session_run_hook as session_run_hook, training_util as training_util
from tensorflow.python.training.session_run_hook import SessionRunArgs as SessionRunArgs
from tensorflow.python.training.summary_io import SummaryWriterCache as SummaryWriterCache
from tensorflow.python.util.tf_export import tf_export as tf_export
from typing import Any

class _HookTimer:
    def __init__(self) -> None: ...
    def reset(self) -> None: ...
    def should_trigger_for_step(self, step) -> None: ...
    def update_last_triggered_step(self, step) -> None: ...
    def last_triggered_step(self) -> None: ...

class SecondOrStepTimer(_HookTimer):
    def __init__(self, every_secs: Any | None = ..., every_steps: Any | None = ...) -> None: ...
    def reset(self) -> None: ...
    def should_trigger_for_step(self, step): ...
    def update_last_triggered_step(self, step): ...
    def last_triggered_step(self): ...

class NeverTriggerTimer(_HookTimer):
    def should_trigger_for_step(self, step): ...
    def update_last_triggered_step(self, step): ...
    def last_triggered_step(self) -> None: ...

class LoggingTensorHook(session_run_hook.SessionRunHook):
    def __init__(self, tensors, every_n_iter: Any | None = ..., every_n_secs: Any | None = ..., at_end: bool = ..., formatter: Any | None = ...) -> None: ...
    def begin(self) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...
    def end(self, session) -> None: ...

def get_or_create_steps_per_run_variable(): ...

class _MultiStepStopAtStepHook(session_run_hook.SessionRunHook):
    def __init__(self, num_steps: Any | None = ..., last_step: Any | None = ..., steps_per_run: int = ...) -> None: ...
    def begin(self) -> None: ...
    def after_create_session(self, session, coord) -> None: ...
    def after_run(self, run_context, run_values) -> None: ...

class StopAtStepHook(session_run_hook.SessionRunHook):
    def __init__(self, num_steps: Any | None = ..., last_step: Any | None = ...) -> None: ...
    def begin(self) -> None: ...
    def after_create_session(self, session, coord) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...

class CheckpointSaverListener:
    def begin(self) -> None: ...
    def before_save(self, session, global_step_value) -> None: ...
    def after_save(self, session, global_step_value) -> None: ...
    def end(self, session, global_step_value) -> None: ...

class CheckpointSaverHook(session_run_hook.SessionRunHook):
    def __init__(self, checkpoint_dir, save_secs: Any | None = ..., save_steps: Any | None = ..., saver: Any | None = ..., checkpoint_basename: str = ..., scaffold: Any | None = ..., listeners: Any | None = ..., save_graph_def: bool = ...) -> None: ...
    def begin(self) -> None: ...
    def after_create_session(self, session, coord) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...
    def end(self, session) -> None: ...

class StepCounterHook(session_run_hook.SessionRunHook):
    def __init__(self, every_n_steps: int = ..., every_n_secs: Any | None = ..., output_dir: Any | None = ..., summary_writer: Any | None = ...) -> None: ...
    def begin(self) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...

class NanLossDuringTrainingError(RuntimeError): ...

class NanTensorHook(session_run_hook.SessionRunHook):
    def __init__(self, loss_tensor, fail_on_nan_loss: bool = ...) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...

class SummarySaverHook(session_run_hook.SessionRunHook):
    def __init__(self, save_steps: Any | None = ..., save_secs: Any | None = ..., output_dir: Any | None = ..., summary_writer: Any | None = ..., scaffold: Any | None = ..., summary_op: Any | None = ...) -> None: ...
    def begin(self) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...
    def end(self, session: Any | None = ...) -> None: ...

class GlobalStepWaiterHook(session_run_hook.SessionRunHook):
    def __init__(self, wait_until_step) -> None: ...
    def begin(self) -> None: ...
    def before_run(self, run_context) -> None: ...

class FinalOpsHook(session_run_hook.SessionRunHook):
    def __init__(self, final_ops, final_ops_feed_dict: Any | None = ...) -> None: ...
    @property
    def final_ops_values(self): ...
    def end(self, session) -> None: ...

class FeedFnHook(session_run_hook.SessionRunHook):
    feed_fn: Any
    def __init__(self, feed_fn) -> None: ...
    def before_run(self, run_context): ...

class ProfilerHook(session_run_hook.SessionRunHook):
    def __init__(self, save_steps: Any | None = ..., save_secs: Any | None = ..., output_dir: str = ..., show_dataflow: bool = ..., show_memory: bool = ...) -> None: ...
    def begin(self) -> None: ...
    def before_run(self, run_context): ...
    def after_run(self, run_context, run_values) -> None: ...
