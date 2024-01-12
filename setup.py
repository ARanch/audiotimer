from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='audiotimer',
    version='0.3.0',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'audiotimer=audiotimer.__main__:main'
        ]
    },
    install_requires=[
        'numpy>=1.26.3',
        'PyAudio>=0.2.14',
        'pynput>=1.7.6'
    ]
)
