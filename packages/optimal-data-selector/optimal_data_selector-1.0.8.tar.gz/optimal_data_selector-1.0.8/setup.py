from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0.8'
DESCRIPTION = 'A Package for to optimize models, use for nlp short word treatment, choosing optimal data for ML models, use for Image Scraping also '
LONG_DESCRIPTION = 'A package to increase the accuracy of ML models, gives you the best data for model training, works on text data also, short word treatment for NLP problems, can be used for Image Scraping also'

# Setting up
setup(
    name="optimal_data_selector",
    version=VERSION,
    author="Rohan Majumder",
    author_email="majumderrohan2001@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['get_best_data_combination', 'optimise_accuracy', 'lock_data_combination', 'gives_best_result', 'best_data_for_ML_models', 'works on text data also','short word treatment','Image Scraping','Web Image Scraping'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)