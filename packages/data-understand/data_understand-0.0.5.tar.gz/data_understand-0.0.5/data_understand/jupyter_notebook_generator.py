"""Module to generate jupyter notebook."""

from pathlib import Path
from typing import Any

import nbformat
from nbformat import v4

import data_understand
from data_understand.class_imbalance import \
    get_jupyter_nb_code_to_find_target_column_imbalance
from data_understand.dataset_characteristics import (
    get_jupyter_nb_code_to_dataframe_head,
    get_jupyter_nb_code_to_dataframe_types,
    get_jupyter_nb_code_to_find_columns_having_missing_values)
from data_understand.dataset_statistics import (
    get_jupyter_nb_code_to_dataframe_num_cols,
    get_jupyter_nb_code_to_dataframe_num_rows)
from data_understand.feature_correlation import (
    get_jupyter_nb_code_to_generate_correlation_matrices,
    get_jupyter_nb_code_to_get_negatively_correlated_feature_pairs,
    get_jupyter_nb_code_to_get_postively_correlated_feature_pairs)
from data_understand.load_dataset import \
    get_jupyter_nb_code_to_read_as_dataframe
from data_understand.messages import (BOX_PLOT_DISTRIBUTION_MESSAGE,
                                      CATEGORICAL_DISTRIBUTION_MESSAGE,
                                      CLASS_IMBALANCE_MESSAGE,
                                      DATA_CHARATERISTICS_MESSAGE,
                                      DATA_VISUALIZATION_MESSAGE,
                                      FEATURE_CORRELATION_GRAPH_MESSAGE,
                                      FEATURE_CORRELATION_MESSAGE,
                                      MAIN_MESSAGE,
                                      NUMERICAL_VALUE_DISTRIBUTION_MESSAGE,
                                      REFERENCES_MESSAGE)
from data_understand.target_characteristics import (
    get_jupyter_nb_code_to_get_ml_task_type, get_jupyter_nb_code_to_get_target)
from data_understand.utils import measure_time
from data_understand.value_distributions import (
    get_jupyter_nb_code_to_generate_box_plot_distributions,
    get_jupyter_nb_code_to_generate_cat_frequency_distributions,
    get_jupyter_nb_code_to_generate_histogram_distributions)


@measure_time
def generate_jupyter_notebook(args: Any) -> None:
    """Generate a jupyter notebook from user parameters.

    :param args: The user parameters.
    :type args: Any
    :return: None
    :rtype: None
    """
    print("Generating jupyter notebook for the dataset in " + args.file_name)
    nb = v4.new_notebook()
    nb.metadata["title"] = "Understanding the data in " + \
        Path(args.file_name).name

    (
        dataframe_read_markdown,
        dataframe_read_code,
    ) = get_jupyter_nb_code_to_read_as_dataframe(Path(args.file_name).name)
    (
        target_read_markdown,
        target_read_code,
    ) = get_jupyter_nb_code_to_get_target(args.target_column)
    (
        ml_task_type_read_markdown,
        ml_task_type_read_code,
    ) = get_jupyter_nb_code_to_get_ml_task_type(args.target_column)
    (
        dataframe_rows_markdown,
        dataframe_rows_code,
    ) = get_jupyter_nb_code_to_dataframe_num_rows()
    (
        dataframe_cols_markdown,
        dataframe_cols_code,
    ) = get_jupyter_nb_code_to_dataframe_num_cols()
    (
        dataframe_types_markdown,
        dataframe_types_code,
    ) = get_jupyter_nb_code_to_dataframe_types()
    (
        dataframe_head_markdown,
        dataframe_head_code,
    ) = get_jupyter_nb_code_to_dataframe_head()
    (
        missing_values_markdown,
        missing_values_code,
    ) = get_jupyter_nb_code_to_find_columns_having_missing_values()

    (
        historgram_markdown,
        histogram_code,
    ) = get_jupyter_nb_code_to_generate_histogram_distributions()
    (
        box_plot_markdown,
        box_plot_code,
    ) = get_jupyter_nb_code_to_generate_box_plot_distributions()
    (
        frequency_markdown,
        frequency_code,
    ) = get_jupyter_nb_code_to_generate_cat_frequency_distributions()

    (
        positive_correlation_markdown,
        positive_correlation_code,
    ) = get_jupyter_nb_code_to_get_postively_correlated_feature_pairs()
    (
        negative_correlation_markdown,
        negative_correlation_code,
    ) = get_jupyter_nb_code_to_get_negatively_correlated_feature_pairs()
    (
        feature_correlation_markdown,
        feature_correlation_code,
    ) = get_jupyter_nb_code_to_generate_correlation_matrices()

    (
        class_imbalance_markdown,
        class_imbalance_code,
    ) = get_jupyter_nb_code_to_find_target_column_imbalance()
    nb["cells"] = [
        v4.new_markdown_cell(
            source="# Understanding the data in " + Path(args.file_name).name
        ),
        v4.new_markdown_cell(
            source=MAIN_MESSAGE.format(
                "jupyter notebook", data_understand.version, "data-understand"
            )
        ),
        v4.new_markdown_cell(source="## Read dataset and set target column"),
        v4.new_markdown_cell(source=dataframe_read_markdown),
        v4.new_code_cell(source=dataframe_read_code),
        v4.new_markdown_cell(source=target_read_markdown),
        v4.new_code_cell(source=target_read_code),
        v4.new_markdown_cell(
            source=(
                "## Display dataset statistics and characteristics\n"
                + DATA_CHARATERISTICS_MESSAGE
            )
        ),
        v4.new_markdown_cell(source=dataframe_rows_markdown),
        v4.new_code_cell(source=dataframe_rows_code),
        v4.new_markdown_cell(source=dataframe_cols_markdown),
        v4.new_code_cell(source=dataframe_cols_code),
        v4.new_markdown_cell(source=dataframe_types_markdown),
        v4.new_code_cell(source=dataframe_types_code),
        v4.new_markdown_cell(source=missing_values_markdown),
        v4.new_code_cell(source=missing_values_code),
        v4.new_markdown_cell(source=dataframe_head_markdown),
        v4.new_code_cell(source=dataframe_head_code),
        v4.new_markdown_cell(source=ml_task_type_read_markdown),
        v4.new_code_cell(source=ml_task_type_read_code),
        v4.new_markdown_cell(
            source="## Visualize distributions of the dataset\n"
            + DATA_VISUALIZATION_MESSAGE
        ),
        v4.new_markdown_cell(
            source=(
                historgram_markdown
                + "\n"
                + NUMERICAL_VALUE_DISTRIBUTION_MESSAGE
            )
        ),
        v4.new_code_cell(source=histogram_code),
        v4.new_markdown_cell(
            source=(
                frequency_markdown + "\n" + CATEGORICAL_DISTRIBUTION_MESSAGE
            )
        ),
        v4.new_code_cell(source=frequency_code),
        v4.new_markdown_cell(
            source=(box_plot_markdown + "\n" + BOX_PLOT_DISTRIBUTION_MESSAGE)
        ),
        v4.new_code_cell(source=box_plot_code),
        v4.new_markdown_cell(
            source=("## Feature Correlations\n" + FEATURE_CORRELATION_MESSAGE)
        ),
        v4.new_markdown_cell(source=positive_correlation_markdown),
        v4.new_code_cell(source=positive_correlation_code),
        v4.new_markdown_cell(source=negative_correlation_markdown),
        v4.new_code_cell(source=negative_correlation_code),
        v4.new_markdown_cell(
            source=(
                feature_correlation_markdown
                + "\n"
                + FEATURE_CORRELATION_GRAPH_MESSAGE
            )
        ),
        v4.new_code_cell(source=feature_correlation_code),
        v4.new_markdown_cell(
            source=(
                "## Find target column imbalances in "
                "classification scenarios\n" + CLASS_IMBALANCE_MESSAGE
            )
        ),
        v4.new_markdown_cell(source=class_imbalance_markdown),
        v4.new_code_cell(source=class_imbalance_code),
        v4.new_markdown_cell(source="## References\n" + REFERENCES_MESSAGE),
    ]

    with open(args.file_name + ".ipynb", "w") as f:
        nbformat.write(nb, f)
    print(
        "Successfully generated jupyter notebook for the dataset in "
        + args.file_name
        + " at "
        + f.name
    )
