from .._core import HueMapping as HueMapping, SemanticMapping as SemanticMapping, SizeMapping as SizeMapping, StyleMapping as StyleMapping, VectorPlotter as VectorPlotter, categorical_order as categorical_order, infer_orient as infer_orient, unique_dashes as unique_dashes, unique_markers as unique_markers, variable_type as variable_type
from ..axisgrid import FacetGrid as FacetGrid
from ..palettes import color_palette as color_palette

class TestSemanticMapping:
    def test_call_lookup(self) -> None: ...

class TestHueMapping:
    def test_init_from_map(self, long_df) -> None: ...
    def test_plotter_default_init(self, long_df) -> None: ...
    def test_plotter_reinit(self, long_df) -> None: ...
    def test_hue_map_null(self, flat_series, null_series) -> None: ...
    def test_hue_map_categorical(self, wide_df, long_df) -> None: ...
    def test_hue_map_numeric(self, long_df) -> None: ...

class TestSizeMapping:
    def test_init_from_map(self, long_df) -> None: ...
    def test_plotter_default_init(self, long_df) -> None: ...
    def test_plotter_reinit(self, long_df) -> None: ...
    def test_size_map_null(self, flat_series, null_series) -> None: ...
    def test_map_size_numeric(self, long_df) -> None: ...
    def test_map_size_categorical(self, long_df) -> None: ...

class TestStyleMapping:
    def test_init_from_map(self, long_df) -> None: ...
    def test_plotter_default_init(self, long_df) -> None: ...
    def test_plotter_reinit(self, long_df) -> None: ...
    def test_style_map_null(self, flat_series, null_series) -> None: ...
    def test_map_style(self, long_df) -> None: ...

class TestVectorPlotter:
    def test_flat_variables(self, flat_data) -> None: ...
    def test_long_numeric_name(self, long_df, name) -> None: ...
    def test_long_hierarchical_index(self, rng) -> None: ...
    def test_long_scalar_and_data(self, long_df) -> None: ...
    def test_wide_semantic_error(self, wide_df) -> None: ...
    def test_long_unknown_error(self, long_df) -> None: ...
    def test_long_unmatched_size_error(self, long_df, flat_array) -> None: ...
    def test_wide_categorical_columns(self, wide_df) -> None: ...
    def test_iter_data_quantitites(self, long_df) -> None: ...
    def test_iter_data_keys(self, long_df) -> None: ...
    def test_iter_data_values(self, long_df) -> None: ...
    def test_iter_data_reverse(self, long_df) -> None: ...
    def test_axis_labels(self, long_df) -> None: ...
    def test_attach_basics(self, long_df, variables) -> None: ...
    def test_attach_disallowed(self, long_df) -> None: ...
    def test_attach_log_scale(self, long_df) -> None: ...
    def test_attach_converters(self, long_df) -> None: ...
    def test_attach_facets(self, long_df) -> None: ...
    def test_get_axes_single(self, long_df) -> None: ...
    def test_get_axes_facets(self, long_df) -> None: ...
    def test_comp_data(self, long_df) -> None: ...
    def test_comp_data_log(self, long_df) -> None: ...
    def test_comp_data_category_order(self) -> None: ...
    def comp_data_missing_fixture(self, request): ...
    def test_comp_data_missing(self, comp_data_missing_fixture) -> None: ...
    def test_var_order(self, long_df) -> None: ...

class TestCoreFunc:
    def test_unique_dashes(self) -> None: ...
    def test_unique_markers(self) -> None: ...
    def test_variable_type(self) -> None: ...
    def test_infer_orient(self) -> None: ...
    def test_categorical_order(self) -> None: ...
