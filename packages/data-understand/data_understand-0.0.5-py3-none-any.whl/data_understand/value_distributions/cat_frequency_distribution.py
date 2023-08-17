"""Module for computing categorical frequency distributions."""

from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

from data_understand.utils import construct_image_name


def _generate_cat_frequency(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """Generate frequency distribution for categorical features.

    :param df: The dataframe to be analyzed.
    :type df: pd.DataFrame
    :return: A dictionary of value counts for each categorical feature.
    :rtype: Dict[str, pd.Series]
    """
    numeric_features = set(df.select_dtypes(include="number").columns.tolist())
    all_features = set(df.columns.tolist())
    categorical_features = list(all_features - numeric_features)

    value_counts_dict = {}
    for feature in categorical_features:
        counts = df[feature].value_counts()
        value_counts_dict[feature] = counts

    return value_counts_dict


def generate_cat_frequency_distributions(df: pd.DataFrame) -> None:
    """Generate frequency distribution for categorical features.

    :param df: The dataframe to be analyzed.
    :type df: pd.DataFrame
    :return: None
    :rtype: None
    """
    value_counts_dict = _generate_cat_frequency(df)
    for key in value_counts_dict:
        value_counts_dict[key].plot(kind="bar")
        plt.title("Frequency of Categories")
        plt.xlabel(key)
        plt.ylabel("Count")
        plt.show()


def save_cat_frequency_distributions(
    df: pd.DataFrame, current_execution_uuid: str
) -> List[str]:
    """Generate and save frequency distribution for categorical features.

    :param df: The dataframe to be analyzed.
    :type df: pd.DataFrame
    :param current_execution_uuid: The current execution UUID.
    :type current_execution_uuid: str
    :return: A list of saved image names.
    :rtype: List[str]
    """
    value_counts_dict = _generate_cat_frequency(df)
    index = 0
    saved_image_name_list = []

    for key in value_counts_dict:
        value_counts_dict[key].plot(kind="bar")
        plt.title("Frequency of Categories")
        plt.xlabel(key)
        plt.ylabel("Count")

        saved_image_name = construct_image_name(
            "cat_frequency", current_execution_uuid, index
        )
        plt.savefig(saved_image_name)
        saved_image_name_list.append(saved_image_name)
        index += 1
        plt.clf()

    return saved_image_name_list


def get_jupyter_nb_code_to_generate_cat_frequency_distributions() -> (
    Tuple[str, str]
):
    """Get code & markdown for frequency distribution of categorical features.

    :return: A tuple of markdown and code snippet.
    :rtype: Tuple[str, str]
    """
    markdown = "### Generate frequency distribution for categorical features"
    code = (
        "from data_understand.value_distributions import "
        + "generate_cat_frequency_distributions\n"
        + "generate_cat_frequency_distributions(df)"
    )
    return markdown, code
