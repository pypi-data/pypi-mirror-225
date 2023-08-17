"""Module for finding different charateristics about dataset."""

from typing import Any, List, Tuple

import numpy as np
import pandas as pd

from data_understand.utils import get_numerical_categorical_features


def _get_columns_having_missing_values(df: pd.DataFrame) -> List[str]:
    """Return the columns having missing values in the dataframe.

    param df: The dataframe to be checked for missing values.
    type df: pandas.DataFrame
    return: The list of columns having missing values.
    rtype: list
    """
    columns_having_missing_values = []
    for feature in df.columns.tolist():
        if np.any(df[feature].isnull()):
            columns_having_missing_values.append(feature)
    return columns_having_missing_values


def get_message_columns_having_missing_values(df: pd.DataFrame) -> str:
    """Get the message about columns having missing values in the dataframe.

    param df: The dataframe to be checked for missing values.
    type df: pandas.DataFrame
    return: The message about the columns having missing values.
    rtype: str
    """
    columns_having_missing_values = _get_columns_having_missing_values(df)
    if len(columns_having_missing_values) == 0:
        return "No columns were found to have missing values"
    else:
        message = "The columns having missing values are: {0}.\n".format(
            ",".join(columns_having_missing_values)
        )
        (
            numerical_feature_list,
            _,
        ) = get_numerical_categorical_features(df)
        for column in columns_having_missing_values:
            if column in numerical_feature_list:
                message += (
                    "- The missing values in column {0} "
                    "could be imputed with mean/median value.\n").format(
                        column
                )
            else:
                message += (
                    "- The missing values in column {0} "
                    "could be imputed with mode value.\n").format(
                        column
                )

        return message


def find_columns_having_missing_values(df: pd.DataFrame) -> None:
    """Print the columns having missing values in the dataframe.

    param df: The dataframe to be checked for missing values.
    type df: pandas.DataFrame
    return: None
    """
    print(get_message_columns_having_missing_values(df))


def get_column_types_as_tuple(df: pd.DataFrame) -> Tuple[Tuple[Any]]:
    """Return the column names and their types as a tuple of tuples.

    param df: The input dataframe.
    type df: pandas.DataFrame
    return: The column names and their types as a tuple of tuples.
    rtype: tuple[tuple[Any]]
    """
    columns = []
    types = []
    tuple_pairs = [("Column", "Type")]
    for key in df.dtypes.to_dict():
        columns.append(key)
        types.append(str(df.dtypes.to_dict()[key]))
        tuple_pairs.append((key, str(df.dtypes.to_dict()[key])))

    return tuple(tuple_pairs)


def get_jupyter_nb_code_to_dataframe_types() -> Tuple[str, str]:
    """Return the markdown and code for displaying the types of dataset.

    return: The markdown and code for displaying the types of dataset.
    rtype: tuple[str, str]
    """
    markdown = "### Display the types of dataset."
    code = "df.dtypes"
    return markdown, code


def get_jupyter_nb_code_to_dataframe_head() -> Tuple[str, str]:
    """Return the markdown and code for displaying the first rows of dataset.

    return: The markdown and code for displaying the first ten
            rows of dataset.
    rtype: tuple[str, str]
    """
    markdown = "### Display the first ten rows of dataset."
    code = "df.head(10)"
    return markdown, code


def get_jupyter_nb_code_to_find_columns_having_missing_values() -> (
    Tuple[str, str]
):
    """Get the markdown and code for finding columns having missing values.

    return: The markdown and code for finding the columns having
            missing values.
    rtype: tuple[str, str]
    """
    markdown = "### Find if any features having missing values"
    code = (
        "from data_understand.dataset_characteristics import "
        + "find_columns_having_missing_values\n"
        + "find_columns_having_missing_values(df)"
    )
    return markdown, code
