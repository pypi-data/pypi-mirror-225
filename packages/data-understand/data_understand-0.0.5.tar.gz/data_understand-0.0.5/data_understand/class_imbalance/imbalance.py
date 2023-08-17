"""Module for computing imbalance in target column."""

from typing import Tuple

import numpy as np
import pandas as pd

from data_understand.utils import get_ml_task_type


def get_message_target_column_imbalance(
    df: pd.DataFrame, target_column: str
) -> str:
    """Get message for target column imbalance.

    param df: The dataframe to be analyzed.
    type df: pandas.core.frame.DataFrame
    param target_column: The name of the target column.
    type target_column: str
    return: The message for target column imbalance.
    rtype: str
    """
    if get_ml_task_type(df, target_column) == "Regression":
        return (
            "The target column values look to be continous in nature. "
            + "So cannot report class imbalance."
        )

    target_column_array = df[target_column].values
    unique_array, element_counts = np.unique(
        target_column_array, return_counts=True
    )

    max_class_count = max(element_counts)
    max_class = unique_array[
        np.argwhere(element_counts == max_class_count)[0][0]
    ]

    output_str = "The summary of number of instances of each class is below\n"
    for element, count in zip(unique_array, element_counts):
        output_str += (
            "- The number of instances of class {0} are: {1}\n".format(
                element, count
            )
        )

    output_str += "\n"
    output_str += "The majority class is: {0}\n".format(max_class)
    for element, count in zip(unique_array, element_counts):
        if max_class != element:
            output_str += (
                "- The ratio of number of instances of majority "
                + "class {0} to class {1} is: {2}\n".format(
                    max_class, element, max_class_count / count
                )
            )

    return output_str


def find_target_column_imbalance(df: pd.DataFrame, target_column: str) -> None:
    """Find if there is any class imbalance in the dataset for classification.

    param df: The dataframe to be analyzed.
    type df: pandas.core.frame.DataFrame
    param target_column: The name of the target column.
    type target_column: str
    return: None
    """
    print(get_message_target_column_imbalance(df, target_column))


def get_jupyter_nb_code_to_find_target_column_imbalance() -> Tuple[str, str]:
    """Get jupyter notebook code to find target column imbalance.

    return: The markdown and code for jupyter notebook.
    rtype: tuple[str, str]
    """
    markdown = (
        "### Find if there is any class imbalance in the "
        + "dataset for classification scenarios."
    )
    code = (
        "from data_understand.class_imbalance import "
        + "find_target_column_imbalance\n"
        + "find_target_column_imbalance(df, target_column)"
    )
    return markdown, code
