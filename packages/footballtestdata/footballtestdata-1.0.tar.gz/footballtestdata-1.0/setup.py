from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'A package to generate fake footballer data'
LONG_DESCRIPTION = 'A package to generate fake footballer data and statistics for data science training purpose'

setup(
    name='footballtestdata',
    version='1.0',
    description='A package to generate fake footballer data and statistics',
    author='Marek Zarzycki',
    author_email='contact@mazarzycki.com',
    author_website='https://mazarzycki.com/',
    packages=find_packages(),

    keywords=['python', 'football', 'soccer', 'data'],

)
