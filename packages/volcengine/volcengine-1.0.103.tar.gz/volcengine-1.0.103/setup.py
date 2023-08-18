# coding:utf-8
import sys

from setuptools import setup, find_packages
from volcengine import VERSION

install_requires = [
    "requests",
    "retry",
    "pytz",
    "pycryptodome==3.9.9",
    "protobuf>=3.20.3",
    "google>=3.0.0",
    "six>=1.0"
]

setup(
    name="volcengine",
    version=VERSION,
    keywords=("pip", "volcengine", "volc-sdk-python"),
    description="The Volcengine SDK for Python",
    license="MIT Licence",

    url="https://github.com/Volcengine/volc-sdk-python",
    author="Volcengine SDK",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=install_requires
)
