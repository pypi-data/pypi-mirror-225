"""Module for loading dataset."""

from typing import Tuple

import pandas as pd


def load_dataset_as_dataframe(file_name: str) -> pd.DataFrame:
    """Load a dataset as a pandas dataframe.

    param file_name: The name of the file to load.
    type file_name: str
    return: The dataset as a pandas dataframe.
    rtype: pd.DataFrame
    """
    return pd.read_csv(file_name)


def get_jupyter_nb_code_to_read_as_dataframe(
    file_name: str,
) -> Tuple[str, str]:
    """Get the code to read dataset as pandas dataframe in a Jupyter notebook.

    param file_name: The name of the file to load.
    type file_name: str
    return: The markdown and code to read the dataset as a pandas dataframe.
    rtype: Tuple[str, str]
    """
    markdown = "### Read the csv file as pandas dataframe"
    code = "import pandas as pd\ndf = pd.read_csv('{0}')".format(file_name)
    return markdown, code
