# Author: yokoe <kreuz45@kreuz45.com>
# Copyright (c) 2023- yokoe
# Licence: MIT

from setuptools import setup

DESCRIPTION = "stowrap: Python Storage Service Wrapper."
NAME = "stowrap"
AUTHOR = "yokoe"
AUTHOR_EMAIL = "kreuz45@kreuz45.com"
URL = "https://github.com/yokoe/stowrap"
LICENSE = "MIT"
DOWNLOAD_URL = URL
VERSION = "0.0.5"
PYTHON_REQUIRES = ">=3.9"
INSTALL_REQUIRES = [
    "gcshus",
    "boto3",
]
PACKAGES = ["stowrap"]
PACKAGE_DIR = {"": "src"}
KEYWORDS = "gcs s3"
CLASSIFIERS = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.9",
]
with open("README.md", "r", encoding="utf-8") as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    packages=PACKAGES,
    package_dir=PACKAGE_DIR,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES,
)
