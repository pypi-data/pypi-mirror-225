"""Module for computing target column characteristics."""

from typing import Tuple


def get_jupyter_nb_code_to_get_target(target_column: str) -> Tuple[str, str]:
    """Return the code to get the target column from the dataframe.

    param target_column: The name of the target column.
    type target_column: str
    return: The markdown and code to get the target column from the dataframe
    rtype: Tuple[str, str]
    """
    markdown = "### Set the target column name"
    code = "target_column = '{}'".format(target_column)
    return markdown, code


def get_jupyter_nb_code_to_get_ml_task_type(
    target_column: str,
) -> Tuple[str, str]:
    """Return the code to get the machine learning task from the target column.

    param target_column: The name of the target column.
    type target_column: str
    return: The markdown and code to get the machine learning task
        from the target column
    rtype: Tuple[str, str]
    """
    markdown = "### Get the machine learning task type"
    code = (
        "from data_understand.utils import get_ml_task_type\n"
        + "get_ml_task_type(df, target_column='{}')".format(target_column)
    )
    return markdown, code
