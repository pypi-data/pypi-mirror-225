from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Define package metadata
VERSION = '1.2'
DESCRIPTION = 'A package to generate fake footballer data'
LONG_DESCRIPTION = 'A package to generate fake footballer data and statistics for data science training purpose'
AUTHOR = 'Marek Zarzycki'
AUTHOR_EMAIL = 'contact@mazarzycki.com'
AUTHOR_WEBSITE = 'https://mazarzycki.com/'

# Define classifiers for your package
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

setup(
    name='footballtestdata',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=AUTHOR_WEBSITE,
    packages=find_packages(),
    classifiers=CLASSIFIERS,  # Add your classifiers here
    keywords=['python', 'football', 'soccer', 'data'],
)
