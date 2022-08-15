from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

setup(
    name="metazerse",
    version="0.0.1",  # Required
    packages=find_packages(exclude=["contrib", "docs", "tests"]),  # Required
    python_requires=">=3.9",
    install_requires=[],  # Optional
    extras_require={},
)
