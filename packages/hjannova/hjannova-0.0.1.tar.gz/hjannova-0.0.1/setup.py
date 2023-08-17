from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'ANOVA TEST'
LONG_DESCRIPTION = "The ANOVA Test Package is a Python library designed to facilitate the analysis of variance (ANOVA) tests, an essential statistical technique used to compare means among multiple groups. Whether you're a data scientist, researcher, or analyst, this package simplifies the process of conducting one-way ANOVA tests, making it easy to determine whether there are statistically significant differences between group means."

# Setting up
setup(
    name="hjannova",
    version=VERSION,
    author="Harshwardhan Jadhav",
    author_email="harshwardhanpj2001@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas','scipy'],
    keywords=['annovatest', 'feature selection', 'annova test', 'python tutorial', 'hj annova test'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)