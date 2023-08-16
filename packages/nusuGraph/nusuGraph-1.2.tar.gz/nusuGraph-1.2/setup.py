"""
@author: Nusab Taha
@contact: https://nusab19.pages.dev/
@license: MIT License, see LICENSE file

Copyright (C) 2023 - Present
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = "1.2"


with open("README.md") as f:
    long_description = f.read()
    long_description = "Will be added..."


setup(
    name="nusuGraph",
    version=version,

    author="Nusab Taha",

    author_email="telegraph@Nusab Taha.pw",
    url="https://github.com/Nusab19/nusuGraph",

    description="Telegraph API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",

    download_url="https://github.com/Nusab19/nusuGraph/archive/v{}.zip".format(
        version
    ),
    license="MIT",

    packages=["nusugraph"],
    install_requires=["httpx"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)
