from tensorflow.python import keras as keras
from tensorflow.python.compat import v2_compat as v2_compat
from tensorflow.python.ops.ragged import ragged_tensor as ragged_tensor
from tensorflow.python.platform import test as tf_test
from typing import Any

class LayerBenchmark(tf_test.Benchmark):
    def report(self, name, keras_time, fc_time, iters) -> None: ...

class StepTimingCallback(keras.callbacks.Callback):
    t0: Any
    steps: int
    def __init__(self) -> None: ...
    def on_predict_batch_begin(self, batch_index, _) -> None: ...
    tn: Any
    t_avg: Any
    def on_predict_end(self, _) -> None: ...

def create_data(length, num_entries, max_value, dtype): ...
def create_string_data(length, num_entries, vocabulary, pct_oov, oov_string: str = ...): ...
def create_vocabulary(vocab_size): ...
def run_keras(data, model, batch_size, num_runs, steps_per_repeat: int = ...): ...
def run_fc(data, fc_fn, batch_size, num_runs, steps_per_repeat: int = ...): ...
