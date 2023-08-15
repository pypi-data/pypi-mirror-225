from matplotlib._image import *
import matplotlib.cm as cm
import matplotlib.artist as martist
from matplotlib.backend_bases import FigureCanvasBase as FigureCanvasBase
from matplotlib.transforms import Affine2D as Affine2D, Bbox as Bbox, BboxBase as BboxBase, BboxTransform as BboxTransform, BboxTransformTo as BboxTransformTo, IdentityTransform as IdentityTransform, TransformedBbox as TransformedBbox
from typing import Any

interpolations_names: Any

def composite_images(images, renderer, magnification: float = ...): ...

class _ImageBase(martist.Artist, cm.ScalarMappable):
    zorder: int
    origin: Any
    axes: Any
    def __init__(self, ax, cmap: Any | None = ..., norm: Any | None = ..., interpolation: Any | None = ..., origin: Any | None = ..., filternorm: bool = ..., filterrad: float = ..., resample: bool = ..., *, interpolation_stage: Any | None = ..., **kwargs) -> None: ...
    def get_size(self): ...
    def set_alpha(self, alpha) -> None: ...
    def changed(self) -> None: ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...) -> None: ...
    stale: bool
    def draw(self, renderer, *args, **kwargs) -> None: ...
    def contains(self, mouseevent): ...
    def write_png(self, fname) -> None: ...
    def set_data(self, A) -> None: ...
    def set_array(self, A) -> None: ...
    def get_interpolation(self): ...
    def set_interpolation(self, s) -> None: ...
    def set_interpolation_stage(self, s) -> None: ...
    def can_composite(self): ...
    def set_resample(self, v) -> None: ...
    def get_resample(self): ...
    def set_filternorm(self, filternorm) -> None: ...
    def get_filternorm(self): ...
    def set_filterrad(self, filterrad) -> None: ...
    def get_filterrad(self): ...

class AxesImage(_ImageBase):
    def __init__(self, ax, cmap: Any | None = ..., norm: Any | None = ..., interpolation: Any | None = ..., origin: Any | None = ..., extent: Any | None = ..., filternorm: bool = ..., filterrad: float = ..., resample: bool = ..., *, interpolation_stage: Any | None = ..., **kwargs) -> None: ...
    def get_window_extent(self, renderer: Any | None = ...): ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...): ...
    stale: bool
    def set_extent(self, extent) -> None: ...
    def get_extent(self): ...
    def get_cursor_data(self, event): ...

class NonUniformImage(AxesImage):
    mouseover: bool
    def __init__(self, ax, *, interpolation: str = ..., **kwargs) -> None: ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...): ...
    stale: bool
    def set_data(self, x, y, A) -> None: ...
    def set_array(self, *args) -> None: ...
    def set_interpolation(self, s) -> None: ...
    def get_extent(self): ...
    def set_filternorm(self, s) -> None: ...
    def set_filterrad(self, s) -> None: ...
    def set_norm(self, norm) -> None: ...
    def set_cmap(self, cmap) -> None: ...

class PcolorImage(AxesImage):
    def __init__(self, ax, x: Any | None = ..., y: Any | None = ..., A: Any | None = ..., cmap: Any | None = ..., norm: Any | None = ..., **kwargs) -> None: ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...): ...
    stale: bool
    def set_data(self, x, y, A) -> None: ...
    def set_array(self, *args) -> None: ...
    def get_cursor_data(self, event): ...

class FigureImage(_ImageBase):
    zorder: int
    figure: Any
    ox: Any
    oy: Any
    magnification: float
    def __init__(self, fig, cmap: Any | None = ..., norm: Any | None = ..., offsetx: int = ..., offsety: int = ..., origin: Any | None = ..., **kwargs) -> None: ...
    def get_extent(self): ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...): ...
    stale: bool
    def set_data(self, A) -> None: ...

class BboxImage(_ImageBase):
    bbox: Any
    def __init__(self, bbox, cmap: Any | None = ..., norm: Any | None = ..., interpolation: Any | None = ..., origin: Any | None = ..., filternorm: bool = ..., filterrad: float = ..., resample: bool = ..., **kwargs) -> None: ...
    def get_window_extent(self, renderer: Any | None = ...): ...
    def contains(self, mouseevent): ...
    def make_image(self, renderer, magnification: float = ..., unsampled: bool = ...): ...

def imread(fname, format: Any | None = ...): ...
def imsave(fname, arr, vmin: Any | None = ..., vmax: Any | None = ..., cmap: Any | None = ..., format: Any | None = ..., origin: Any | None = ..., dpi: int = ..., *, metadata: Any | None = ..., pil_kwargs: Any | None = ...) -> None: ...
def pil_to_array(pilImage): ...
def thumbnail(infile, thumbfile, scale: float = ..., interpolation: str = ..., preview: bool = ...): ...
