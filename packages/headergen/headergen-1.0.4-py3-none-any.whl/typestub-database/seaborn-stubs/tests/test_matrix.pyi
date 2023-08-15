from .. import color_palette as color_palette
from .._testing import assert_colors_equal as assert_colors_equal
from typing import Any

class TestHeatmap:
    rs: Any
    x_norm: Any
    letters: Any
    df_norm: Any
    x_unif: Any
    df_unif: Any
    default_kws: Any
    def test_ndarray_input(self) -> None: ...
    def test_df_input(self) -> None: ...
    def test_df_multindex_input(self) -> None: ...
    def test_mask_input(self, dtype) -> None: ...
    def test_mask_limits(self) -> None: ...
    def test_default_vlims(self) -> None: ...
    def test_robust_vlims(self) -> None: ...
    def test_custom_sequential_vlims(self) -> None: ...
    def test_custom_diverging_vlims(self) -> None: ...
    def test_array_with_nans(self) -> None: ...
    def test_mask(self) -> None: ...
    def test_custom_cmap(self) -> None: ...
    def test_centered_vlims(self) -> None: ...
    def test_default_colors(self) -> None: ...
    def test_custom_vlim_colors(self) -> None: ...
    def test_custom_center_colors(self) -> None: ...
    def test_cmap_with_properties(self) -> None: ...
    def test_tickabels_off(self) -> None: ...
    def test_custom_ticklabels(self) -> None: ...
    def test_custom_ticklabel_interval(self) -> None: ...
    def test_heatmap_annotation(self) -> None: ...
    def test_heatmap_annotation_overwrite_kws(self) -> None: ...
    def test_heatmap_annotation_with_mask(self) -> None: ...
    def test_heatmap_annotation_mesh_colors(self) -> None: ...
    def test_heatmap_annotation_other_data(self) -> None: ...
    def test_heatmap_annotation_with_limited_ticklabels(self) -> None: ...
    def test_heatmap_cbar(self) -> None: ...
    def test_heatmap_axes(self) -> None: ...
    def test_heatmap_ticklabel_rotation(self) -> None: ...
    def test_heatmap_inner_lines(self) -> None: ...
    def test_square_aspect(self) -> None: ...
    def test_mask_validation(self) -> None: ...
    def test_missing_data_mask(self) -> None: ...
    def test_cbar_ticks(self) -> None: ...

class TestDendrogram:
    rs: Any
    x_norm: Any
    letters: Any
    df_norm: Any
    x_norm_linkage: Any
    x_norm_distances: Any
    x_norm_dendrogram: Any
    x_norm_leaves: Any
    df_norm_leaves: Any
    default_kws: Any
    def test_ndarray_input(self) -> None: ...
    def test_df_input(self) -> None: ...
    def test_df_multindex_input(self) -> None: ...
    def test_axis0_input(self) -> None: ...
    def test_rotate_input(self) -> None: ...
    def test_rotate_axis0_input(self) -> None: ...
    def test_custom_linkage(self) -> None: ...
    def test_label_false(self) -> None: ...
    def test_linkage_scipy(self) -> None: ...
    def test_fastcluster_other_method(self) -> None: ...
    def test_fastcluster_non_euclidean(self) -> None: ...
    def test_dendrogram_plot(self) -> None: ...
    def test_dendrogram_rotate(self) -> None: ...
    def test_dendrogram_ticklabel_rotation(self) -> None: ...

class TestClustermap:
    rs: Any
    x_norm: Any
    letters: Any
    df_norm: Any
    x_norm_linkage: Any
    x_norm_distances: Any
    x_norm_dendrogram: Any
    x_norm_leaves: Any
    df_norm_leaves: Any
    default_kws: Any
    default_plot_kws: Any
    row_colors: Any
    col_colors: Any
    def test_ndarray_input(self) -> None: ...
    def test_df_input(self) -> None: ...
    def test_corr_df_input(self) -> None: ...
    def test_pivot_input(self) -> None: ...
    def test_colors_input(self) -> None: ...
    def test_categorical_colors_input(self) -> None: ...
    def test_nested_colors_input(self) -> None: ...
    def test_colors_input_custom_cmap(self) -> None: ...
    def test_z_score(self) -> None: ...
    def test_z_score_axis0(self) -> None: ...
    def test_standard_scale(self) -> None: ...
    def test_standard_scale_axis0(self) -> None: ...
    def test_z_score_standard_scale(self) -> None: ...
    def test_color_list_to_matrix_and_cmap(self) -> None: ...
    def test_nested_color_list_to_matrix_and_cmap(self) -> None: ...
    def test_color_list_to_matrix_and_cmap_axis1(self) -> None: ...
    def test_color_list_to_matrix_and_cmap_different_sizes(self) -> None: ...
    def test_savefig(self) -> None: ...
    def test_plot_dendrograms(self) -> None: ...
    def test_cluster_false(self) -> None: ...
    def test_row_col_colors(self) -> None: ...
    def test_cluster_false_row_col_colors(self) -> None: ...
    def test_row_col_colors_df(self) -> None: ...
    def test_row_col_colors_df_shuffled(self) -> None: ...
    def test_row_col_colors_df_missing(self) -> None: ...
    def test_row_col_colors_df_one_axis(self) -> None: ...
    def test_row_col_colors_series(self) -> None: ...
    def test_row_col_colors_series_shuffled(self) -> None: ...
    def test_row_col_colors_series_missing(self) -> None: ...
    def test_row_col_colors_ignore_heatmap_kwargs(self) -> None: ...
    def test_row_col_colors_raise_on_mixed_index_types(self) -> None: ...
    def test_mask_reorganization(self) -> None: ...
    def test_ticklabel_reorganization(self) -> None: ...
    def test_noticklabels(self) -> None: ...
    def test_size_ratios(self) -> None: ...
    def test_cbar_pos(self) -> None: ...
    def test_square_warning(self) -> None: ...
    def test_clustermap_annotation(self) -> None: ...
    def test_tree_kws(self) -> None: ...
