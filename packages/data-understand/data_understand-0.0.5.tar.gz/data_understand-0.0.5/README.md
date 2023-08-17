# data-understand
![PyPI data-understand](https://img.shields.io/pypi/v/data-understand)
[![Downloads](https://static.pepy.tech/badge/data-understand)](https://pepy.tech/project/data-understand)
[![Run Python E2E Tests](https://github.com/ggupta2005/data.understand/actions/workflows/python-e2e-tests.yml/badge.svg)](https://github.com/ggupta2005/data.understand/actions/workflows/python-e2e-tests.yml)
[![Run Python Unit Tests](https://github.com/ggupta2005/data.understand/actions/workflows/python-unit-tests.yml/badge.svg)](https://github.com/ggupta2005/data.understand/actions/workflows/python-unit-tests.yml)

## Motivation
As data scientists and machine learning engineers, we are often required to execute various data science tasks like loading up the dataset into a pandas dataframe, inspecting the columns/rows in the dataset, visualizing the distribution of values, finding feature correlations and determining if there are any sort of imbalances in the dataset. Often these tasks are repetitive and involve creating multiple jupyter notebooks and we have to manage these jupyter notebooks separately with different handles to the location of input dataset. How about you have one tool which could take the directory location of your dataset and generate the boring aforementioned logic for you to execute and learn the same insights about your dataset. All you need to do is to install this tool in your local python environment and then execute the tool from a command line.

## Installation
You can install the package `data-understand` from pypi using the following command:-

```
pip install data-understand
```

## Usage
Once you have installed the tool locally, you can then look at the various options of the CLI tool:-

```
data_understand -h
========================================================================================================================
========================================================================================================================
usage: data_understand [-h] [-f FILE_NAME] [-t TARGET_COLUMN] [-p] [-j]

data.understand CLI

options:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        Directory path to CSV file
  -t TARGET_COLUMN, --target_column TARGET_COLUMN
                        Target column name
  -p, --generate_pdf    Generate PDF file for understanding of data
  -j, --generate_jupyter_notebook
                        Generate jupyter notebook file for understanding of data
```

## Notebook and PDF report generation
In order to generate both PDF report and jupyter notebook you can execute the following CLI command:-

```
data_understand --file_name adult_dataset.csv --target_column income --generate_pdf --generate_jupyter_notebook
========================================================================================================================
========================================================================================================================
The parsed arguments are:- 
file_name: adult_dataset.csv
target_column: income
generate_pdf: True
generate_jupyter_notebook: True
Time taken: 0.0 min 0.0012356000000863787 sec
========================================================================================================================
Generating PDF report and jupyter notebook
========================================================================================================================
Generating PDF report for the dataset in adult_dataset.csv
Successfully generated PDF report for the dataset in adult_dataset.csv at adult_dataset.csv.pdf
Time taken: 0.0 min 7.363417799999979 sec
========================================================================================================================
========================================================================================================================
Generating jupyter notebook for the dataset in adult_dataset.csv
Successfully generated jupyter notebook for the dataset in adult_dataset.csv at adult_dataset.csv.ipynb
Time taken: 0.0 min 0.053841799999986506 sec
========================================================================================================================
Successfully generated PDF report and jupyter notebook
Time taken: 0.0 min 7.485209299999951 sec
========================================================================================================================
```

This would generate the jupyter notebook and PDF report in the same directory location as your dataset. You can execute the cells in the jupyter notebook to generate various insights and graphs on the fly or you can read through the PDF report to learn about various aspects of your dataset.

## Repos using `data-understand` to generate notebooks and PDF reports
- [understanding-datasets](https://github.com/ggupta2005/understanding-datasets)
