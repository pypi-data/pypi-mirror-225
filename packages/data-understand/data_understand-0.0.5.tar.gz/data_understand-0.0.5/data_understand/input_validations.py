"""Module for validating the user input parameters."""

import os
from typing import Any

import pandas as pd
from raiutils.exceptions import UserErrorException


def validate_input_parameters(args: Any) -> None:
    """Validate the input parameters.

    The function validates the input parameters and raises an exception if
    the input parameters are not valid. The function validates the following
    parameters:

    1. The file name is not None.
    2. The target column name is not None.
    3. The file name is a CSV file.
    4. The file name exists.
    5. Able to read the file as a pandas DataFrame.
    6. The target column name exists in the dataset.

    param args: The input parameters.
    type args: Any
    return: None
    """
    # Read all parameters
    file_name = args.file_name
    target_column = args.target_column

    if file_name is None:
        raise UserErrorException(
            "A valid file name {0} is required. "
            "Please provide a valid file path.".format(args.file_name)
        )

    if target_column is None:
        raise UserErrorException("A valid target column name is required.")

    if not isinstance(file_name, str):
        raise UserErrorException("The file_name given is not string")

    if not file_name.endswith(".csv"):
        raise UserErrorException(
            "The file {} is not a CSV file. "
            "Please provide a CSV file.".format(file_name)
        )

    if not os.path.exists(file_name):
        raise UserErrorException(
            "The file {} doesn't exists.".format(file_name)
        )

    try:
        df = pd.read_csv(file_name)
    except Exception:
        raise UserErrorException(
            "Unable to read CSV file {0} as a pandas DataFrame".format(
                file_name
            )
        )

    if target_column not in df.columns.tolist():
        raise UserErrorException(
            "The target column name {0} doesn't exist in dataset.".format(
                target_column
            )
        )
