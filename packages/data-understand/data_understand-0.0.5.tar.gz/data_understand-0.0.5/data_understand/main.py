"""Main entry point of data.understand."""

import argparse
import warnings

from data_understand.input_validations import validate_input_parameters
from data_understand.jupyter_notebook_generator import \
    generate_jupyter_notebook
from data_understand.pdf_generator import generate_pdf
from data_understand.utils import measure_time


@measure_time
def parse_args() -> None:
    """Parse input arguments provided by the user."""
    # Create Argument Parser
    parser = argparse.ArgumentParser(description="data.understand CLI")

    # Define Arguments
    parser.add_argument("-f", "--file_name", help="Directory path to CSV file")
    parser.add_argument(
        "-t", "--target_column", help="Target column name", default=None
    )
    parser.add_argument(
        "-p",
        "--generate_pdf",
        help="Generate PDF file for understanding of data",
        action="store_true",
    )
    parser.add_argument(
        "-j",
        "--generate_jupyter_notebook",
        help="Generate jupyter notebook file for understanding of data",
        action="store_true",
    )

    # Parse Arguments
    args = parser.parse_args()

    # Access Parsed Values
    print("The parsed arguments are:- ")
    print("file_name: " + str(args.file_name))
    print("target_column: " + str(args.target_column))
    print("generate_pdf: " + str(args.generate_pdf))
    print("generate_jupyter_notebook: " + str(args.generate_jupyter_notebook))

    return args


@measure_time
def main():
    """Generate data.understand artifacts based on user inputs."""
    warnings.filterwarnings("ignore")
    args = parse_args()
    validate_input_parameters(args)
    print("Generating PDF report and jupyter notebook")
    if args.generate_pdf:
        generate_pdf(args)

    if args.generate_jupyter_notebook:
        generate_jupyter_notebook(args)
    print("Successfully generated PDF report and jupyter notebook")


if __name__ == "__main__":
    main()
