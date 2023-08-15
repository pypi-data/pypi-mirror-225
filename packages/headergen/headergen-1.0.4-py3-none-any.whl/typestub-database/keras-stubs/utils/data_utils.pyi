import abc
from abc import abstractmethod
from keras.utils import io_utils as io_utils, tf_inspect as tf_inspect
from keras.utils.generic_utils import Progbar as Progbar
from typing import Any

def urlretrieve(url, filename, reporthook: Any | None = ..., data: Any | None = ...) -> None: ...
def is_generator_or_sequence(x): ...
def get_file(fname: Any | None = ..., origin: Any | None = ..., untar: bool = ..., md5_hash: Any | None = ..., file_hash: Any | None = ..., cache_subdir: str = ..., hash_algorithm: str = ..., extract: bool = ..., archive_format: str = ..., cache_dir: Any | None = ...): ...
def validate_file(fpath, file_hash, algorithm: str = ..., chunk_size: int = ...): ...

class ThreadsafeIter:
    it: Any
    lock: Any
    def __init__(self, it) -> None: ...
    def __iter__(self): ...
    def next(self): ...
    def __next__(self): ...

def threadsafe_generator(f): ...

class Sequence(metaclass=abc.ABCMeta):
    @abstractmethod
    def __getitem__(self, index): ...
    @abstractmethod
    def __len__(self): ...
    def on_epoch_end(self) -> None: ...
    def __iter__(self): ...

def iter_sequence_infinite(seq) -> None: ...
def dont_use_multiprocessing_pool(f): ...
def get_pool_class(use_multiprocessing): ...
def get_worker_id_queue(): ...
def init_pool(seqs) -> None: ...
def get_index(uid, i): ...

class SequenceEnqueuer(metaclass=abc.ABCMeta):
    sequence: Any
    use_multiprocessing: Any
    uid: Any
    workers: int
    executor_fn: Any
    queue: Any
    run_thread: Any
    stop_signal: Any
    def __init__(self, sequence, use_multiprocessing: bool = ...) -> None: ...
    def is_running(self): ...
    def start(self, workers: int = ..., max_queue_size: int = ...): ...
    def stop(self, timeout: Any | None = ...) -> None: ...
    def __del__(self) -> None: ...
    @abstractmethod
    def get(self): ...

class OrderedEnqueuer(SequenceEnqueuer):
    shuffle: Any
    def __init__(self, sequence, use_multiprocessing: bool = ..., shuffle: bool = ...) -> None: ...
    def get(self) -> None: ...

def init_pool_generator(gens, random_seed: Any | None = ..., id_queue: Any | None = ...) -> None: ...
def next_sample(uid): ...

class GeneratorEnqueuer(SequenceEnqueuer):
    random_seed: Any
    def __init__(self, generator, use_multiprocessing: bool = ..., random_seed: Any | None = ...) -> None: ...
    def get(self) -> None: ...
