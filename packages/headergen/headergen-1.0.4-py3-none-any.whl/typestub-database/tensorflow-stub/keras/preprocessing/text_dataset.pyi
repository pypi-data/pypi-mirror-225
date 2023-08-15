from tensorflow.python.data.ops import dataset_ops as dataset_ops
from tensorflow.python.keras.preprocessing import dataset_utils as dataset_utils
from tensorflow.python.ops import io_ops as io_ops, string_ops as string_ops
from tensorflow.python.util.tf_export import keras_export as keras_export
from typing import Any

def text_dataset_from_directory(directory, labels: str = ..., label_mode: str = ..., class_names: Any | None = ..., batch_size: int = ..., max_length: Any | None = ..., shuffle: bool = ..., seed: Any | None = ..., validation_split: Any | None = ..., subset: Any | None = ..., follow_links: bool = ...): ...
def paths_and_labels_to_dataset(file_paths, labels, label_mode, num_classes, max_length): ...
def path_to_string_content(path, max_length): ...
