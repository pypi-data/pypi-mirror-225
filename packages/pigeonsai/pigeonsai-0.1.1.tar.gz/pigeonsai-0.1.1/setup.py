#!/usr/bin/env python
#
# Copyright (c) 2020-2021 PigeonsAI Inc. All right reserved.
#

import os
from setuptools import setup, find_packages

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), encoding="utf-8") as f:
        return f.read()

long_desc = """
PigeonsAI is an ecosystem to build production ready machine learning applications.
"""

setup(
    name="pigeonsai",
    version="0.1.1",
    description="PigeonAI client and SDK",
    license="Proprietary License",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://www.pigeonsai.com/",
    project_urls={
        "Homepage": "https://www.pigeonsai.com",
        "Documentation": "https://docs.pigeonsai.com/",
        "Contact": "https://pigeonsai.com/",
    },
    author="PigeonsAI Inc.",
    author_email="info@pigeonsai.com",
    keywords="PigeonsAI AI ecosystem vector database cloud semantic search",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
