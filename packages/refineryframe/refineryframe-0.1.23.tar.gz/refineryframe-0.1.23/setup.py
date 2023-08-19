from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

base_packages = [
    "attrs>=22.2.0",
    "datetime",
    "pandas",
    "numpy",
    "unidecode"
]

VERSION = '0.1.23'
DESCRIPTION = 'Cleans data, best to be used as a part of initial preprocessor'
LONG_DESCRIPTION = 'A package that allows to detect unexpected values in data and clean them according to set of predefined rules'

# Setting up
setup(
    name="refineryframe",
    #use_scm_version=True,
    version=VERSION,
    author="Kyrylo Mordan",
    author_email="<parachute.repo@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=base_packages,
    keywords=['python', 'data cleaning', 'safeguards'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
    ]
)
