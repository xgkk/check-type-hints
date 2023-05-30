from setuptools import setup, find_packages

setup(
    name="check-type-hints",
    version="0.0.1",
    description="Helps you check type hints when you commit code.",
    install_requires=['typer', ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'check_type_hints=check_type_hints.main:app'
        ]
    }
)
