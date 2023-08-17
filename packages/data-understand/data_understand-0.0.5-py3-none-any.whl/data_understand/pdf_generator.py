"""Module to generate PDF report."""

import os
import uuid
from pathlib import Path
from typing import Any, List, Tuple

from fpdf import FPDF, Align

import data_understand
from data_understand.class_imbalance import get_message_target_column_imbalance
from data_understand.dataset_characteristics.characteristics import (
    get_column_types_as_tuple, get_message_columns_having_missing_values)
from data_understand.feature_correlation import (
    get_feature_correlations_as_tuple, save_correlation_matrices)
from data_understand.load_dataset import load_dataset_as_dataframe
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
from data_understand.utils import get_ml_task_type, measure_time
from data_understand.value_distributions import (
    save_box_plot_distributions, save_cat_frequency_distributions,
    save_histogram_distributions)


class PDFReportGenerator(FPDF):
    """This class is responsible for generating a PDF report for given dataset.

    The report contains the following information:-
    1. Dataset characteristics
    2. Visualize distributions of the dataset
    3. Feature correlations between numerical features
    4. Class Imbalance
    """

    def __init__(self, file_name, target_column_name) -> None:
        """Initialize the PDFReportGenerator class.

        :param file_name: The name of the .csv file to be analyzed.
        :type file_name: str
        :param target_column_name: The name of the target column.
        :type target_column_name: str
        :return: None
        :rtype: None
        """
        super(PDFReportGenerator, self).__init__()
        self._file_name = file_name
        self._target_column_name = target_column_name
        self._dataframe = load_dataset_as_dataframe(file_name)
        self._current_execution_uuid = str(uuid.uuid4())

    def header(self) -> None:
        """Add watermark in each page of the PDF report.

        :return: None
        :rtype: None
        """
        # Add watermark in the header
        self.set_font("Arial", "B", 50)
        self.set_text_color(128, 128, 128)
        self.rotate(45)
        self.text(-50, 150, "data.understand")
        self.rotate(0)
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "", 12)

    def footer(self) -> None:
        """Add page number in each page of the PDF report.

        :return: None
        :rtype: None
        """
        self.set_y(-15)  # Position the footer 15 units from the bottom
        self.set_font("Arial", size=11)  # Set font and style for the footer
        self.cell(
            0, 10, f"{self.page_no()}", 0, 0, "C"
        )  # Print the page number centered

    def _add_heading(self, message: str) -> None:
        """Add a heading to the PDF report.

        :param message: The message to be added as a heading.
        :type message: str
        :return: None
        :rtype: None
        """
        self.set_font("Arial", size=20)
        self.cell(200, 10, message, align="C")
        self.ln()

    def _add_sub_heading(self, message: str) -> None:
        """Add a sub heading to the PDF report.

        :param message: The message to be added as a sub heading.
        :type message: str
        :return: None
        :rtype: None
        """
        self.set_font("Arial", size=15)
        self.cell(None, None, message)
        self.ln()

    def _add_text(self, message: str, multi_line=False) -> None:
        """Add a text to the PDF report.

        :param message: The message to be added as a text.
        :type message: str
        :param multi_line: A boolean flag indicating whether the message is a
            multi line message or not.
        :type multi_line: bool
        :return: None
        :rtype: None
        """
        self.set_font("Arial", size=11)
        if multi_line:
            self.multi_cell(0, 10, message, markdown=True)
        else:
            self.cell(0, 10, message)
        self.ln()

    def _add_table(
        self, message: str, dataset_as_tuples: Tuple[Tuple[Any]]
    ) -> None:
        """Add a table to the PDF report.

        :param message: The message to be added before the table.
        :type message: str
        :param dataset_as_tuples: The dataset to be added as a table.
        :type dataset_as_tuples: Tuple[Tuple[Any]]
        :return: None
        :rtype: None
        """
        self._add_text(message)
        with self.table(text_align="CENTER") as table:
            for data_row in dataset_as_tuples:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
        self.ln()

    def add_title_and_description_page(self) -> None:
        """Add the title and description page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading(
            message="Understanding the data in " + Path(self._file_name).name
        )
        self._add_text(
            message=MAIN_MESSAGE.format(
                "PDF report", data_understand.version, "data-understand"
            ),
            multi_line=True,
        )

    def add_index_page(self) -> None:
        """Add the index page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_sub_heading(message="Index")
        self._add_text("Chapter 1 - Dataset Charateristics")
        self._add_text("Chapter 2 - Visualize distributions of the dataset")
        self._add_text(
            "Chapter 3 - Feature correlations between numerical features"
        )
        self._add_text("Chapter 4 - Class Imbalance")

    def add_data_characteristics_page(self) -> None:
        """Add the dataset characteristics page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading("Chapter 1 - Dataset Charateristics")

        self._add_text(message=DATA_CHARATERISTICS_MESSAGE, multi_line=True)
        self._add_text(
            "The number of rows in the dataset are: "
            + str(self._dataframe.shape[0])
        )

        self._add_text(
            "The number of columns in the dataset are: "
            + str(self._dataframe.shape[1]),
        )

        self._add_text(
            "The name of the target column is: " + self._target_column_name,
        )

        self._add_text(
            "The machine learning task based on your target column looks like: "
            + get_ml_task_type(self._dataframe, self._target_column_name)
        )

        self._add_text(
            get_message_columns_having_missing_values(self._dataframe),
            multi_line=True,
        )

        dataset_snapshot_table = get_column_types_as_tuple(self._dataframe)
        self._add_table(
            "The table of data type for each column is below:-",
            dataset_snapshot_table,
        )

    def add_data_visualization_pages(self) -> None:
        """Add the data visualization pages to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading("Chapter 2 - Visualize distributions of the dataset")
        self._add_text(DATA_VISUALIZATION_MESSAGE, multi_line=True)
        self._add_cat_frequency_page()
        self._add_value_distribution_page()
        self._add_box_plot_page()

    def _add_cat_frequency_page(self) -> None:
        """Add the categorical frequency page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_sub_heading("Categorical feature distribution")
        self._add_text(CATEGORICAL_DISTRIBUTION_MESSAGE, multi_line=True)
        saved_file_name_list = save_cat_frequency_distributions(
            self._dataframe, self._current_execution_uuid
        )

        self._add_multiple_images(
            saved_file_name_list=saved_file_name_list,
            title="Categorical value distribution",
        )

        if len(saved_file_name_list) == 0:
            self._add_text("No categorical features exists in the dataset.")

    def _add_multiple_images(
        self, saved_file_name_list: List[str], title: str
    ) -> None:
        """Add multiple images to the PDF report.

        :param saved_file_name_list: The list of saved file names.
        :type saved_file_name_list: List[str]
        :param title: The title of the image.
        :type title: str
        :return: None
        :rtype: None
        """
        index = 0
        page_index = 0
        while index < len(saved_file_name_list):
            if index > 0 and index % 4 == 0:
                self.add_page()
                page_index = 0

            if page_index % 2 == 0:
                self.image(
                    saved_file_name_list[index],
                    Align.L,
                    y=60 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title=title,
                )
            else:
                self.image(
                    saved_file_name_list[index],
                    Align.R,
                    y=60 + (page_index // 2) * 90,
                    w=90,
                    h=90,
                    title=title,
                )
            os.remove(saved_file_name_list[index])

            page_index += 1
            index += 1

    def _add_value_distribution_page(self) -> None:
        """Add the numerical value distribution page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_sub_heading("Numerical value distribution")
        self._add_text(NUMERICAL_VALUE_DISTRIBUTION_MESSAGE, multi_line=True)
        saved_file_name_list = save_histogram_distributions(
            self._dataframe, self._current_execution_uuid
        )

        self._add_multiple_images(
            saved_file_name_list=saved_file_name_list,
            title="Numerical value distribution",
        )

        if len(saved_file_name_list) == 0:
            self._add_text("No numerical features exists in the dataset.")

    def _add_box_plot_page(self) -> None:
        """Add the box plot page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_sub_heading("Box plot distribution")
        self._add_text(BOX_PLOT_DISTRIBUTION_MESSAGE, multi_line=True)
        saved_file_name_list = save_box_plot_distributions(
            self._dataframe, self._current_execution_uuid
        )

        self._add_multiple_images(
            saved_file_name_list=saved_file_name_list,
            title="Box Plot distribution",
        )

        if len(saved_file_name_list) == 0:
            self._add_text("No categorical features exists in the dataset.")

    def add_feature_correlation_page(self) -> None:
        """Add the feature correlation page to the PDF report.

        return: None
        rtype: None
        """
        self._add_feature_correlation_page()

    def _add_feature_correlation_page(self) -> None:
        """Add the feature correlation page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading(
            "Chapter 3 - Feature correlations between numerical features"
        )
        self._add_text(FEATURE_CORRELATION_MESSAGE, multi_line=True)

        positive_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, True
        )
        self._add_table(
            "Top five positive feature correlations",
            positive_feature_correlation_table,
        )

        negative_feature_correlation_table = get_feature_correlations_as_tuple(
            self._dataframe, 5, False
        )
        self._add_table(
            "Top five negative feature correlations",
            negative_feature_correlation_table,
        )

        self.add_page()
        self._add_text(FEATURE_CORRELATION_GRAPH_MESSAGE, multi_line=True)
        saved_file_name = save_correlation_matrices(
            self._dataframe, self._current_execution_uuid
        )
        # Add the image to the page
        self.image(
            saved_file_name,
            Align.C,
            y=30,
            w=200,
            h=200,
            title="Correlation plots for numeric features",
        )
        os.remove(saved_file_name)

    def add_class_imbalance_page(self) -> None:
        """Add the class imbalance page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading("Chapter 4 - Class Imbalance")
        self._add_text(CLASS_IMBALANCE_MESSAGE, multi_line=True)
        self._add_text(
            get_message_target_column_imbalance(
                self._dataframe, self._target_column_name
            ),
            multi_line=True,
        )

    def add_references_page(self) -> None:
        """Add the reference page to the PDF report.

        return: None
        rtype: None
        """
        self.add_page()
        self._add_heading("References")
        self._add_text(REFERENCES_MESSAGE, multi_line=True)

    def save_pdf(self) -> None:
        """Save the PDF report.

        return: None
        rtype: None
        """
        self.output(self._file_name + ".pdf")


@measure_time
def generate_pdf(args: Any) -> None:
    """Generate the PDF report for the dataset.

    :param args: The user parameters.
    :type args: Any
    :return: None
    :rtype: None
    """
    print("Generating PDF report for the dataset in " + args.file_name)
    pdf_report_generator = PDFReportGenerator(
        args.file_name, args.target_column
    )
    pdf_report_generator.add_title_and_description_page()
    pdf_report_generator.add_index_page()
    pdf_report_generator.add_data_characteristics_page()
    pdf_report_generator.add_data_visualization_pages()
    pdf_report_generator.add_feature_correlation_page()
    pdf_report_generator.add_class_imbalance_page()
    pdf_report_generator.add_references_page()
    pdf_report_generator.save_pdf()
    print(
        "Successfully generated PDF report for the dataset in "
        + args.file_name
        + " at "
        + args.file_name
        + ".pdf"
    )
