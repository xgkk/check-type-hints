from setuptools import setup, find_packages
version = "0.0.3"
setup(
    name="check-type-hints",
    version=version,
    description="Helps you check type hints when you commit code.",
    install_requires=['typer', ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'check_type_hints=check_type_hints.main:app'
        ]
    }
)
