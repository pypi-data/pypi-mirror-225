from matplotlib._pylab_helpers import Gcf as Gcf
from matplotlib.backend_bases import FigureCanvasBase as FigureCanvasBase, FigureManagerBase as FigureManagerBase, GraphicsContextBase as GraphicsContextBase, RendererBase as RendererBase
from matplotlib.figure import Figure as Figure
from typing import Any

class RendererTemplate(RendererBase):
    dpi: Any
    def __init__(self, dpi) -> None: ...
    def draw_path(self, gc, path, transform, rgbFace: Any | None = ...) -> None: ...
    def draw_image(self, gc, x, y, im) -> None: ...
    def draw_text(self, gc, x, y, s, prop, angle, ismath: bool = ..., mtext: Any | None = ...) -> None: ...
    def flipy(self): ...
    def get_canvas_width_height(self): ...
    def get_text_width_height_descent(self, s, prop, ismath): ...
    def new_gc(self): ...
    def points_to_pixels(self, points): ...

class GraphicsContextTemplate(GraphicsContextBase): ...

def draw_if_interactive() -> None: ...
def show(*, block: Any | None = ...) -> None: ...
def new_figure_manager(num, *args, FigureClass=..., **kwargs): ...
def new_figure_manager_given_figure(num, figure): ...

class FigureCanvasTemplate(FigureCanvasBase):
    def draw(self) -> None: ...
    filetypes: Any
    def print_foo(self, filename, *args, **kwargs) -> None: ...
    def get_default_filetype(self): ...

class FigureManagerTemplate(FigureManagerBase): ...
FigureCanvas = FigureCanvasTemplate
FigureManager = FigureManagerTemplate
