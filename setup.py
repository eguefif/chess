import sys
from setuptools import setup, find_packages

install_requires = []
description = ""
classifiers = [
    "Programming Language :: Python",
]


setup(
    name="chess",
    version="0.0.1",
    url="xxx",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=classifiers,
    install_requires=install_requires,
)
