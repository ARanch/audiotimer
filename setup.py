from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='audiotimer',
    version='0.2.2',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown'
)