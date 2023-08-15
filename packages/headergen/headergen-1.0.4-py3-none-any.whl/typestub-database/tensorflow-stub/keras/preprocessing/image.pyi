from keras_preprocessing import image
from scipy import linalg as linalg, ndimage as ndimage
from tensorflow.python.framework import ops as ops
from tensorflow.python.keras import backend as backend
from tensorflow.python.keras.preprocessing.image_dataset import image_dataset_from_directory as image_dataset_from_directory
from tensorflow.python.keras.utils import data_utils as data_utils, tf_inspect as tf_inspect
from tensorflow.python.ops import array_ops as array_ops, image_ops as image_ops, math_ops as math_ops
from tensorflow.python.platform import tf_logging as tf_logging
from tensorflow.python.util.tf_export import keras_export as keras_export
from typing import Any

random_rotation: Any
random_shift: Any
random_shear: Any
random_zoom: Any
apply_channel_shift: Any
random_channel_shift: Any
apply_brightness_shift: Any
random_brightness: Any
apply_affine_transform: Any

def smart_resize(x, size, interpolation: str = ...): ...
def array_to_img(x, data_format: Any | None = ..., scale: bool = ..., dtype: Any | None = ...): ...
def img_to_array(img, data_format: Any | None = ..., dtype: Any | None = ...): ...
def save_img(path, x, data_format: Any | None = ..., file_format: Any | None = ..., scale: bool = ..., **kwargs) -> None: ...
def load_img(path, grayscale: bool = ..., color_mode: str = ..., target_size: Any | None = ..., interpolation: str = ...): ...

class Iterator(image.Iterator, data_utils.Sequence): ...

class DirectoryIterator(image.DirectoryIterator, Iterator):
    def __init__(self, directory, image_data_generator, target_size=..., color_mode: str = ..., classes: Any | None = ..., class_mode: str = ..., batch_size: int = ..., shuffle: bool = ..., seed: Any | None = ..., data_format: Any | None = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., follow_links: bool = ..., subset: Any | None = ..., interpolation: str = ..., dtype: Any | None = ...) -> None: ...

class NumpyArrayIterator(image.NumpyArrayIterator, Iterator):
    def __init__(self, x, y, image_data_generator, batch_size: int = ..., shuffle: bool = ..., sample_weight: Any | None = ..., seed: Any | None = ..., data_format: Any | None = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., subset: Any | None = ..., dtype: Any | None = ...) -> None: ...

class DataFrameIterator(image.DataFrameIterator, Iterator):
    def __init__(self, dataframe, directory: Any | None = ..., image_data_generator: Any | None = ..., x_col: str = ..., y_col: str = ..., weight_col: Any | None = ..., target_size=..., color_mode: str = ..., classes: Any | None = ..., class_mode: str = ..., batch_size: int = ..., shuffle: bool = ..., seed: Any | None = ..., data_format: str = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., subset: Any | None = ..., interpolation: str = ..., dtype: str = ..., validate_filenames: bool = ...) -> None: ...

class ImageDataGenerator(image.ImageDataGenerator):
    def __init__(self, featurewise_center: bool = ..., samplewise_center: bool = ..., featurewise_std_normalization: bool = ..., samplewise_std_normalization: bool = ..., zca_whitening: bool = ..., zca_epsilon: float = ..., rotation_range: int = ..., width_shift_range: float = ..., height_shift_range: float = ..., brightness_range: Any | None = ..., shear_range: float = ..., zoom_range: float = ..., channel_shift_range: float = ..., fill_mode: str = ..., cval: float = ..., horizontal_flip: bool = ..., vertical_flip: bool = ..., rescale: Any | None = ..., preprocessing_function: Any | None = ..., data_format: Any | None = ..., validation_split: float = ..., dtype: Any | None = ...) -> None: ...
    def flow(self, x, y: Any | None = ..., batch_size: int = ..., shuffle: bool = ..., sample_weight: Any | None = ..., seed: Any | None = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., subset: Any | None = ...): ...
    def flow_from_directory(self, directory, target_size=..., color_mode: str = ..., classes: Any | None = ..., class_mode: str = ..., batch_size: int = ..., shuffle: bool = ..., seed: Any | None = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., follow_links: bool = ..., subset: Any | None = ..., interpolation: str = ...): ...
    def flow_from_dataframe(self, dataframe, directory: Any | None = ..., x_col: str = ..., y_col: str = ..., weight_col: Any | None = ..., target_size=..., color_mode: str = ..., classes: Any | None = ..., class_mode: str = ..., batch_size: int = ..., shuffle: bool = ..., seed: Any | None = ..., save_to_dir: Any | None = ..., save_prefix: str = ..., save_format: str = ..., subset: Any | None = ..., interpolation: str = ..., validate_filenames: bool = ..., **kwargs): ...
