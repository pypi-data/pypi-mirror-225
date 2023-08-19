from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = """
\033[1mdsmate\033[0m: Simplify data tasks in Python with interactive interface for effortless data interaction. Empower your data journey today.
"""
LONG_DESCRIPTION = """
\033[1mIntroducing dsmate: Simplifying Data Processing and Analysis in Python\033[0m

\033[1mdsmate\033[0m is a comprehensive Python library designed to streamline and simplify the entire data manipulation and analysis workflow. With its intuitive classes and interactive interface, \033[1mdsmate\033[0m empowers users to effortlessly handle various data-related tasks, making data preparation, exploration, visualization, and machine learning model creation more accessible than ever before.

\033[1mKey Features:\033[0m

1. \033[1mdfclean\033[0m: Tackle Data Cleaning with Ease
   The \033[1mdfclean\033[0m class offers a powerful solution for managing missing data, handling outliers, scaling features, and categorizing data. Effortlessly preprocess your datasets to ensure they are primed for analysis.

2. \033[1mdfsum\033[0m: Gain Deeper Insights with Data Summarization
   Uncover the essence of your data using the \033[1mdfsum\033[0m class. This functionality allows you to quickly grasp the essential statistics and characteristics of your datasets, facilitating better decision-making.

3. \033[1mdfviz\033[0m: Visualize Data for Enhanced Understanding
   The \033[1mdfviz\033[0m class empowers you to visualize each column in your dataset through a variety of charts, enabling you to grasp patterns, trends, and correlations with ease. Transform raw data into meaningful insights.

4. \033[1mdfload\033[0m: Simplified Loading of Large Datasets
   With the \033[1mdfload\033[0m class, effortlessly load and convert a multitude of files into dataframes. Save time and resources while working with extensive datasets, making the data loading process seamless.

5. \033[1mml_model\033[0m: Effortless Machine Learning Model Creation
   Create and assess machine learning models effortlessly using the \033[1mml_model\033[0m class. Gauge the performance of your models with various algorithms, facilitating informed decision-making in your data-driven projects.

\033[1mInteractive Interface for Enhanced User Experience:\033[0m

\033[1mdsmate\033[0m introduces an interactive interface that leverages windows to provide users with a more engaging and user-friendly environment. This interface streamlines your workflow, allowing you to seamlessly interact with your data, perform tasks, and analyze results in a dynamic and intuitive manner.

Whether you're a data scientist, analyst, or enthusiast, \033[1mdsmate\033[0m is your trusted companion for simplifying the complex world of data manipulation and analysis. Say goodbye to tedious processes and hello to efficiency and insight with \033[1mdsmate\033[0m.

For a better understanding of the library, visit the \033[4mdsmate repository\033[0m: https://github.com/DL4150/dsmate
"""


setup(
    name="dsmate",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Daniel Lawrence",
    author_email="daniellawrence4150@gmail.com",
    url='https://github.com/DL4150/dsmate',
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas','sklearn','scipy','matplotlib','seaborn','numpy'],
    keywords=['python','data science','data analytics','machine learning','data','analysis'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
