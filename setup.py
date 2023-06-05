from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.0.4"
setup(
    name="check-type-hints",
    version=version,
    description="Helps you check type hints when you commit code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "typer",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["check_type_hints=check_type_hints.main:app"]},
)
