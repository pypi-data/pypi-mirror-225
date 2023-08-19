from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    author='workmail20',
    name='pirichain_api_workmail20',
    description = 'Package for base Pirichain API calls',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=['workmail20']),
    python_requires='>=3.7'
)