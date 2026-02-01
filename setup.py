"""Setup configuration for Context Guardian."""

from setuptools import find_packages, setup

setup(
    name="context-guardian",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)
