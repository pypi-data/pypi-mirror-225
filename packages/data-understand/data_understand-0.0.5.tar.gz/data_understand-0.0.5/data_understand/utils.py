"""Utilities module for helper functions."""

import timeit
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

SEPARATOR_LENGTH = 120


def measure_time(compute_func):
    """Measure the time taken by a function to execute via a decorator.

    :param compute_func: Function to be decorated
    :type compute_func: function
    :return: Decorated function
    :rtype: function
    """

    def compute_wrapper(*args, **kwargs):
        """Print the time taken by a function to execute and return result.

        :param args: Arguments to be passed to the function
        :type args: list
        :param kwargs: Keyword arguments to be passed to the function
        :type kwargs: dict
        :return: Result of the function
        :rtype: object
        """
        print(get_separator(SEPARATOR_LENGTH))
        start_time = timeit.default_timer()
        result = compute_func(*args, **kwargs)
        elapsed = timeit.default_timer() - start_time
        m, s = divmod(elapsed, 60)
        print("Time taken: {0} min {1} sec".format(m, s))
        print(get_separator(SEPARATOR_LENGTH))
        return result

    return compute_wrapper


def get_separator(max_len: int) -> str:
    """
    Return a separator string of length max_len.

    :param max_len: Length of the separator string
    :type max_len: int
    :return: Separator string
    :rtype: str
    """
    return "=" * max_len


def get_ml_task_type(df: pd.DataFrame, target_column: str) -> str:
    """
    Return the machine learning task type based on the target column.

    :param df: Dataframe
    :type df: pd.DataFrame
    :param target_column: Name of the target column
    :type target_column: str
    :return: Machine learning task type
    :rtype: str
    """
    target_column_array = df[target_column].values
    unique_array, element_counts = np.unique(
        target_column_array, return_counts=True
    )
    if np.issubdtype(unique_array.dtype, np.number) and len(
        unique_array
    ) > 0.1 * len(target_column_array):
        return "Regression"
    if len(unique_array) == 2:
        return "Binary Classification"
    return "Multiclass Classification"


def get_numerical_categorical_features(
    df: pd.DataFrame,
) -> Tuple[List[str], List[str]]:
    """Get the numerical features and categorical features from a dataframe.

    :param df: The dataframe to get the categorical features from.
    :type df: pd.DataFrame
    :return: A tuple of lists of non-categorical and categorical features.
    :rtype: Tuple[List[str], List[str]]
    """
    numeric_features = set(df.select_dtypes(include="number").columns.tolist())
    all_features = set(df.columns.tolist())
    return numeric_features, list(all_features - numeric_features)


def construct_image_name(
    image_name: str,
    current_execution_uuid: str,
    index: Optional[int] = None,
    extension: Optional[str] = ".png",
):
    """
    Construct the image name and return it.

    :param image_name: Name of the image
    :type image_name: str
    :param current_execution_uuid: Current execution uuid
    :type current_execution_uuid: str
    :param index: Index of the image
    :type index: int
    :param extension: Extension of the image
    :type extension: str
    :return: Constructed image name
    :rtype: str
    """
    if index is not None:
        return (
            image_name
            + "_"
            + current_execution_uuid
            + "_"
            + str(index)
            + extension
        )
    else:
        return image_name + "_" + current_execution_uuid + extension
