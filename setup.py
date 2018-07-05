import os
import sys
from distutils.sysconfig import get_python_lib
from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================
This version of Smart Home Inventory requires Python {}.{}, but you're trying to
install it on Python {}.{}.
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sinventory",
    version="0.0.1",
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    author="Wandering Couple",
    author_email="we@wanderingcouple.in",
    description="A simple home inventory managenemt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dhiman-ghosh/smart-home-inventory",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
    ),
)
