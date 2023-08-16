# coding: utf-8

"""
    Wells Data Pipeline Cores
"""

from setuptools import setup, find_packages  # noqa: H301

NAME = "wells-data-pipeline-cores"
VERSION = "0.1.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3", "requests", "pyyaml", "python-decouple", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Wells Data Pipeline Library",
    author_email="",
    url="",
    keywords=["WellsDataPipeline"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    Wells Data Pipeline Cores Library  # noqa: E501
    """
)
