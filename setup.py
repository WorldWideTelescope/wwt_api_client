#! /usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
# Copyright 2019-2020 the .NET Foundation
# Distributed under the terms of the revised (3-clause) BSD license.

from __future__ import absolute_import, division, print_function

from os.path import join as pjoin
from setuptools import setup

from setupbase import find_packages, get_version

name = "wwt_api_client"  # cranko project-name
version = "0.dev0"  # cranko project-version

with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

setup_args = dict(
    name=name,
    description="An API client for the AAS WorldWide Telescope web services",
    long_description=LONG_DESCRIPTION,
    version=version,
    packages=find_packages(),
    author="Peter K. G. Williams",
    author_email="peter@newton.cx",
    url="https://github.com/WorldWideTelescope/wwt_api_client",
    license="BSD",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Science"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    include_package_data=True,
    install_requires=[
        "requests",
        "six",
    ],
    extras_require={
        "test": [
            "httpretty",
            "pytest",
            "pytest-cov",
            "pytest-mock",
        ],
        "docs": [
            "sphinx>=1.6",
            "sphinx-automodapi",
            "numpydoc",
            "sphinx_rtd_theme",
        ],
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
