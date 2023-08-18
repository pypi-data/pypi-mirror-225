from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.1.9'
DESCRIPTION = 'CellCover'
LONG_DESCRIPTION = 'A package that identifies marker gene panels of single cell RNA-seq data using set covering'

# Setting up
setup(
    name="CellCover",
    version=VERSION,
    author="Laurent Younes",
    author_email="<laurent.younes@jhu.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['gurobipy'],
    keywords=['python', 'single-cell', 'marker gene'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)