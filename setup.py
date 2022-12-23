"""
setup.py

Setup for installing the package.
"""
from setuptools import setup, find_packages
from pathlib import Path

import investments-vc

VERSION = investments-vc.__version__
AUTHOR = investments-vc.__author__
EMAIL = investments-vc.__email__

BASE_DIR = Path(__file__).resolve().parent
README = BASE_DIR.joinpath("README.md")

setup(
    name="investments-vc",
    version=VERSION,
    description="Capstone project that I created as part of CareerERA's Post Graduate Program (investments-vc)",
    long_description=README.read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/clamytoe/investments-vc",
    author=AUTHOR,
    author_email=EMAIL,
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        #   7 - Inactive
        "Development Status :: 1 - Planning",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9.15",
    ],
    keywords="python utility",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["pytest"],
    license="MIT",
    entry_points={
        "console_scripts": [
            "investments-vc=investments-vc.app:main"
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/clamytoe/investments-vc/issues',
        'Source': 'https://github.com/clamytoe/investments-vc/',
    },
)
