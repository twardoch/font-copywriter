#!/usr/bin/env python3

import re
from pathlib import Path

from setuptools import find_packages, setup

NAME = "font_copywriter"


def get_version(*args):
    verstrline = open(Path(NAME, "__init__.py")).read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    return mo[1] if (mo := re.search(VSRE, verstrline, re.M)) else "undefined"


setup(
    name=f"{NAME}",
    version=get_version(),
    description="Tool to make human-readable descriptions of fonts.",
    long_description=open(
        Path(Path(__file__).parent, "README.md"), encoding="utf-8"
    ).read(),
    long_description_content_type="text/markdown",
    keywords=[
        "unicode",
    ],
    url="https://github.com/twardoch/font_copywriter",
    author="Adam Twardoch",
    author_email="adam+github@twardoch.com",
    license="Apache 2.0",
    python_requires=">=3.9",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Text Processing :: Fonts",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
