from .bezier import BezierSegment as BezierSegment
from .cbook import simple_linear_interpolation as simple_linear_interpolation
from typing import Any

class Path:
    code_type: Any
    STOP: Any
    MOVETO: Any
    LINETO: Any
    CURVE3: Any
    CURVE4: Any
    CLOSEPOLY: Any
    NUM_VERTICES_FOR_CODE: Any
    def __init__(self, vertices, codes: Any | None = ..., _interpolation_steps: int = ..., closed: bool = ..., readonly: bool = ...) -> None: ...
    @property
    def vertices(self): ...
    @vertices.setter
    def vertices(self, vertices) -> None: ...
    @property
    def codes(self): ...
    @codes.setter
    def codes(self, codes) -> None: ...
    @property
    def simplify_threshold(self): ...
    @simplify_threshold.setter
    def simplify_threshold(self, threshold) -> None: ...
    @property
    def should_simplify(self): ...
    @should_simplify.setter
    def should_simplify(self, should_simplify) -> None: ...
    @property
    def readonly(self): ...
    def copy(self): ...
    def __deepcopy__(self, memo: Any | None = ...): ...
    deepcopy: Any
    @classmethod
    def make_compound_path_from_polys(cls, XY): ...
    @classmethod
    def make_compound_path(cls, *args): ...
    def __len__(self): ...
    def iter_segments(self, transform: Any | None = ..., remove_nans: bool = ..., clip: Any | None = ..., snap: bool = ..., stroke_width: float = ..., simplify: Any | None = ..., curves: bool = ..., sketch: Any | None = ...) -> None: ...
    def iter_bezier(self, **kwargs) -> None: ...
    def cleaned(self, transform: Any | None = ..., remove_nans: bool = ..., clip: Any | None = ..., *, simplify: bool = ..., curves: bool = ..., stroke_width: float = ..., snap: bool = ..., sketch: Any | None = ...): ...
    def transformed(self, transform): ...
    def contains_point(self, point, transform: Any | None = ..., radius: float = ...): ...
    def contains_points(self, points, transform: Any | None = ..., radius: float = ...): ...
    def contains_path(self, path, transform: Any | None = ...): ...
    def get_extents(self, transform: Any | None = ..., **kwargs): ...
    def intersects_path(self, other, filled: bool = ...): ...
    def intersects_bbox(self, bbox, filled: bool = ...): ...
    def interpolated(self, steps): ...
    def to_polygons(self, transform: Any | None = ..., width: int = ..., height: int = ..., closed_only: bool = ...): ...
    @classmethod
    def unit_rectangle(cls): ...
    @classmethod
    def unit_regular_polygon(cls, numVertices): ...
    @classmethod
    def unit_regular_star(cls, numVertices, innerCircle: float = ...): ...
    @classmethod
    def unit_regular_asterisk(cls, numVertices): ...
    @classmethod
    def unit_circle(cls): ...
    @classmethod
    def circle(cls, center=..., radius: float = ..., readonly: bool = ...): ...
    @classmethod
    def unit_circle_righthalf(cls): ...
    @classmethod
    def arc(cls, theta1, theta2, n: Any | None = ..., is_wedge: bool = ...): ...
    @classmethod
    def wedge(cls, theta1, theta2, n: Any | None = ...): ...
    @staticmethod
    def hatch(hatchpattern, density: int = ...): ...
    def clip_to_bbox(self, bbox, inside: bool = ...): ...

def get_path_collection_extents(master_transform, paths, transforms, offsets, offset_transform): ...
