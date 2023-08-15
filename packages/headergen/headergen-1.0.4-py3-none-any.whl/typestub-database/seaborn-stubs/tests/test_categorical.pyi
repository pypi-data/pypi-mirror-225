from .. import palettes as palettes
from typing import Any

class CategoricalFixture:
    rs: Any
    n_total: int
    x: Any
    x_df: Any
    y: Any
    y_perm: Any
    g: Any
    h: Any
    u: Any
    df: Any

class TestCategoricalPlotter(CategoricalFixture):
    def test_wide_df_data(self) -> None: ...
    def test_1d_input_data(self) -> None: ...
    def test_2d_input_data(self) -> None: ...
    def test_3d_input_data(self) -> None: ...
    def test_list_of_array_input_data(self) -> None: ...
    def test_wide_array_input_data(self) -> None: ...
    def test_single_long_direct_inputs(self) -> None: ...
    def test_single_long_indirect_inputs(self) -> None: ...
    def test_longform_groupby(self) -> None: ...
    def test_input_validation(self) -> None: ...
    def test_order(self) -> None: ...
    def test_hue_order(self) -> None: ...
    def test_plot_units(self) -> None: ...
    def test_default_palettes(self) -> None: ...
    def test_default_palette_with_many_levels(self) -> None: ...
    def test_specific_color(self) -> None: ...
    def test_specific_palette(self) -> None: ...
    def test_dict_as_palette(self) -> None: ...
    def test_palette_desaturation(self) -> None: ...

class TestCategoricalStatPlotter(CategoricalFixture):
    def test_no_bootstrappig(self) -> None: ...
    def test_single_layer_stats(self) -> None: ...
    def test_single_layer_stats_with_units(self) -> None: ...
    def test_single_layer_stats_with_missing_data(self) -> None: ...
    def test_nested_stats(self) -> None: ...
    def test_bootstrap_seed(self) -> None: ...
    def test_nested_stats_with_units(self) -> None: ...
    def test_nested_stats_with_missing_data(self) -> None: ...
    def test_sd_error_bars(self) -> None: ...
    def test_nested_sd_error_bars(self) -> None: ...
    def test_draw_cis(self) -> None: ...

class TestBoxPlotter(CategoricalFixture):
    default_kws: Any
    def test_nested_width(self) -> None: ...
    def test_hue_offsets(self) -> None: ...
    def test_axes_data(self) -> None: ...
    def test_box_colors(self) -> None: ...
    def test_draw_missing_boxes(self) -> None: ...
    def test_missing_data(self) -> None: ...
    def test_unaligned_index(self) -> None: ...
    def test_boxplots(self) -> None: ...
    def test_axes_annotation(self) -> None: ...

class TestViolinPlotter(CategoricalFixture):
    default_kws: Any
    def test_split_error(self) -> None: ...
    def test_no_observations(self) -> None: ...
    def test_single_observation(self) -> None: ...
    def test_dwidth(self) -> None: ...
    def test_scale_area(self) -> None: ...
    def test_scale_width(self) -> None: ...
    def test_scale_count(self) -> None: ...
    def test_bad_scale(self) -> None: ...
    def test_kde_fit(self) -> None: ...
    def test_draw_to_density(self) -> None: ...
    def test_draw_single_observations(self) -> None: ...
    def test_draw_box_lines(self) -> None: ...
    def test_draw_quartiles(self) -> None: ...
    def test_draw_points(self) -> None: ...
    def test_draw_sticks(self) -> None: ...
    def test_validate_inner(self) -> None: ...
    def test_draw_violinplots(self) -> None: ...
    def test_draw_violinplots_no_observations(self) -> None: ...
    def test_draw_violinplots_single_observations(self) -> None: ...
    def test_violinplots(self) -> None: ...

class TestCategoricalScatterPlotter(CategoricalFixture):
    def test_group_point_colors(self) -> None: ...
    def test_hue_point_colors(self) -> None: ...
    def test_scatterplot_legend(self) -> None: ...

class TestStripPlotter(CategoricalFixture):
    def test_stripplot_vertical(self) -> None: ...
    def test_stripplot_horiztonal(self) -> None: ...
    def test_stripplot_jitter(self) -> None: ...
    def test_dodge_nested_stripplot_vertical(self) -> None: ...
    def test_dodge_nested_stripplot_horizontal(self) -> None: ...
    def test_nested_stripplot_vertical(self) -> None: ...
    def test_nested_stripplot_horizontal(self) -> None: ...
    def test_three_strip_points(self) -> None: ...
    def test_unaligned_index(self) -> None: ...

class TestSwarmPlotter(CategoricalFixture):
    default_kws: Any
    def test_could_overlap(self) -> None: ...
    def test_position_candidates(self) -> None: ...
    def test_find_first_non_overlapping_candidate(self) -> None: ...
    def test_beeswarm(self) -> None: ...
    def test_add_gutters(self) -> None: ...
    def test_swarmplot_vertical(self) -> None: ...
    def test_swarmplot_horizontal(self) -> None: ...
    def test_dodge_nested_swarmplot_vertical(self) -> None: ...
    def test_dodge_nested_swarmplot_horizontal(self) -> None: ...
    def test_nested_swarmplot_vertical(self) -> None: ...
    def test_nested_swarmplot_horizontal(self) -> None: ...
    def test_unaligned_index(self) -> None: ...

class TestBarPlotter(CategoricalFixture):
    default_kws: Any
    def test_nested_width(self) -> None: ...
    def test_draw_vertical_bars(self) -> None: ...
    def test_draw_horizontal_bars(self) -> None: ...
    def test_draw_nested_vertical_bars(self) -> None: ...
    def test_draw_nested_horizontal_bars(self) -> None: ...
    def test_draw_missing_bars(self) -> None: ...
    def test_unaligned_index(self) -> None: ...
    def test_barplot_colors(self) -> None: ...
    def test_simple_barplots(self) -> None: ...

class TestPointPlotter(CategoricalFixture):
    default_kws: Any
    def test_different_defualt_colors(self) -> None: ...
    def test_hue_offsets(self) -> None: ...
    def test_draw_vertical_points(self) -> None: ...
    def test_draw_horizontal_points(self) -> None: ...
    def test_draw_vertical_nested_points(self) -> None: ...
    def test_draw_horizontal_nested_points(self) -> None: ...
    def test_draw_missing_points(self) -> None: ...
    def test_unaligned_index(self) -> None: ...
    def test_pointplot_colors(self) -> None: ...
    def test_simple_pointplots(self) -> None: ...

class TestCountPlot(CategoricalFixture):
    def test_plot_elements(self) -> None: ...
    def test_input_error(self) -> None: ...

class TestCatPlot(CategoricalFixture):
    def test_facet_organization(self) -> None: ...
    def test_plot_elements(self) -> None: ...
    def test_bad_plot_kind_error(self) -> None: ...
    def test_count_x_and_y(self) -> None: ...
    def test_plot_colors(self) -> None: ...
    def test_ax_kwarg_removal(self) -> None: ...
    def test_factorplot(self) -> None: ...
    def test_share_xy(self) -> None: ...

class TestBoxenPlotter(CategoricalFixture):
    default_kws: Any
    def ispatch(self, c): ...
    def ispath(self, c): ...
    def edge_calc(self, n, data): ...
    def test_box_ends_finite(self): ...
    def test_box_ends_correct_tukey(self) -> None: ...
    def test_box_ends_correct_proportion(self) -> None: ...
    def test_box_ends_correct_trustworthy(self, n, exp_k) -> None: ...
    def test_outliers(self) -> None: ...
    def test_showfliers(self) -> None: ...
    def test_invalid_depths(self) -> None: ...
    def test_valid_depths(self, power) -> None: ...
    def test_valid_scales(self) -> None: ...
    def test_hue_offsets(self) -> None: ...
    def test_axes_data(self) -> None: ...
    def test_box_colors(self) -> None: ...
    def test_draw_missing_boxes(self) -> None: ...
    def test_unaligned_index(self) -> None: ...
    def test_missing_data(self) -> None: ...
    def test_boxenplots(self) -> None: ...
    def test_axes_annotation(self) -> None: ...
    def test_legend_titlesize(self, size) -> None: ...
    def test_Float64_input(self) -> None: ...
