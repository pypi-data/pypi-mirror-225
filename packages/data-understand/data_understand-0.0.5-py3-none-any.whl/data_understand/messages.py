"""This module maintains the messages displayed to the user."""

from data_understand.constants import URLS

MAIN_MESSAGE = (
    "The {0} provides a comprehensive analysis of "
    "tabular data, focusing on various characteristics such "
    "as data types, number of rows, and number of columns. "
    "By examining these attributes, the report offers "
    "effective understanding of the dataset, enabling data "
    "analysts to gain insights and make informed decisions.\n\n"
    "In addition to descriptive statistics, the {0} "
    "utilizes graphical representations to visualize the "
    "distribution of numerical data and explores feature "
    "correlations. Through correlation plots, the "
    "relationships between different features are analyzed, "
    "revealing potential associations and dependencies "
    "within the dataset. These insights further enhance the "
    "understanding of the data and help identify key "
    "variables that may influence the target outcome.\n\n"
    "The {0} also investigates the distribution of "
    "categories for string features and provides class "
    "imbalance measures for classification scenarios. By "
    "assessing the balance of classes within the dataset, it "
    "highlights potential challenges in training models and "
    "making accurate predictions. This analysis is "
    "particularly valuable in machine learning tasks, as it "
    "helps to identify strategies for handling class "
    "imbalances and improving the performance of "
    "classification algorithms.\n\nThis version of {0} has "
    "been generated from `{1}` version of `{2}`."
)

DATA_CHARATERISTICS_MESSAGE = (
    "In this section we report basic cardinality of the dataset "
    "like number of rows and number of columns. "
    "We report the data types of the columns in the dataset. "
    "Some columns are numeric, representing either integers or "
    "floating-point values. Other columns are categorical, "
    "containing string or object values. Additionally, there may "
    "be datetime columns capturing specific timestamps or dates.\n\n"
    "We also report whether any column in the dataset has missing values. "
    "These missing values indicate instances "
    "where data is not available or was not recorded for certain "
    "records. Identifying and handling these missing values "
    "appropriately is crucial to ensure accurate analysis.\n\n"
    "Furthermore, the nature of the target variable in the dataset "
    "is essential to determine the objective of analysis. If the "
    "target variable is categorical, it implies a classification "
    "problem, where the goal is to assign instances to specific "
    "categories or classes. On the other hand, if the target "
    "variable is numeric or continuous, it signifies a regression "
    "problem, where the focus lies in predicting a numeric value "
    "based on other variables.\n\nUnderstanding these various aspects "
    "of the dataset lays the foundation for further exploration, "
    "analysis, and modeling tasks."
)

DATA_VISUALIZATION_MESSAGE = (
    "This section have different graphs using which you can "
    "visualize distibutions of different features in your dataset, "
    "visualize the distibution of various categories for "
    "categorical features, visualize the histogram distribution "
    "of numerical features and visualize the box plot distribution "
    "between categories in categorical columns and numerical columns."
)

CATEGORICAL_DISTRIBUTION_MESSAGE = (
    "The section shows the distribution of individual categories "
    "in a given categorical column. The distribution helps to "
    "understand which categories in a given column are most/least "
    "prevelant in your dataset."
)

NUMERICAL_VALUE_DISTRIBUTION_MESSAGE = (
    "The section shows the histogram distribution of various "
    "numerical features in your dataset. The graphs also show "
    "a line chart which helps understand how the normal distribution "
    "will look if the numerical values in the distribution were "
    "normally distributed. These graphs also help gauge if the "
    "distibution of data in a particular column in skewed in any "
    "direction."
)

BOX_PLOT_DISTRIBUTION_MESSAGE = (
    "The section shows the box plot distribution of between "
    "the categories in categorical columns and numerical values "
    "in a numerical column. These graphs help in uncovering "
    "patterns that exist between various categories in a "
    "categorical column with the values in the numerical columns."
)

FEATURE_CORRELATION_MESSAGE = (
    "This section shows the numerical feature pairs having "
    "positive and negative correlation. The correlation have been "
    "computed using [Pearson correlation coefficient]"
    "({0}). "
    "Examination of feature correlation can help find if the data "
    "has [leaky features]"
    "({1}).".format(
        URLS["Pearson correlation coefficient"], URLS["leaky features"]
    )
)

FEATURE_CORRELATION_GRAPH_MESSAGE = (
    "Feature correlation graph showing the scatter plot "
    "between any two numerical features. This graph helps to "
    "understand if there are any correlation between numerical "
    "features."
)

CLASS_IMBALANCE_MESSAGE = (
    "In this section we show statistics to bring out the imbalance "
    "between the different classes in the target column for a "
    "classification problem. This will help you learn if you need "
    "to address the issue of [class imbalance]"
    "({0}) in your dataset.".format(URLS["class imbalance"])
)

REFERENCES_MESSAGE = (
    "You can visit the following links for further exploration:- \n"
    "- [data.understand]({0})".format(URLS["data.understand"])
)
