#! /usr/bin/env python
# Copyright 2019-2023 the .NET Foundation
# Distributed under the MIT license

from setuptools import setup


def get_long_desc():
    in_preamble = True
    lines = []

    with open("README.md", "rt", encoding="utf8") as f:
        for line in f:
            if in_preamble:
                if line.startswith("<!--pypi-begin-->"):
                    in_preamble = False
            else:
                if line.startswith("<!--pypi-end-->"):
                    break
                else:
                    lines.append(line)

    lines.append(
        """

For more information, including installation instructions, please visit [the
project homepage].

[the project homepage]: https://wwt-api-client.readthedocs.io/
"""
    )
    return "".join(lines)


setup_args = dict(
    name="wwt_api_client",  # cranko project-name
    version="0.4.0",  # cranko project-version
    description="An API client for the AAS WorldWide Telescope web services",
    long_description=get_long_desc(),
    long_description_content_type="text/markdown",
    author="AAS WorldWide Telescope Team",
    author_email="wwt@aas.org",
    url="https://github.com/WorldWideTelescope/wwt_api_client",
    packages=[
        "wwt_api_client",
        "wwt_api_client.constellations",
        "wwt_api_client.tests",
    ],
    license="MIT",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Science"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    install_requires=[
        "dataclasses-json >=0.5",
        "html-sanitizer",
        "license-expression >=21.6",
        "openidc_client >=0.6",
        "requests >=2.10",
        "wwt_data_formats >=0.16",
    ],
    extras_require={
        "test": [
            "httpretty",
            "mock",
            "pytest",
            "pytest-cov",
            "pytest-mock",
        ],
        "docs": [
            "astropy-sphinx-theme",
            "numpydoc",
            "sphinx",
            "sphinx-automodapi",
        ],
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
