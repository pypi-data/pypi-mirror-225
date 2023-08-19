from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A data science package'
LONG_DESCRIPTION = 'A package that makes it easy to solve basic data science, machine learning or data analytics problems'

setup(
    name="dsmate",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Daniel Lawrence",
    author_email="daniellawrence4150@gmail.com",
    license='MIT',
    packages=find_packages(),
    install_requires=['pandas','tkinter','sklearn','scipy','matplotlib','seaborn','numpy'],
    keywords=['python','data science','data analytics','machine learning','data','analysis'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)
