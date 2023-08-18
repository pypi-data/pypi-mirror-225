from setuptools import setup, find_packages

# Package metadata
PACKAGE_NAME = 'sinum'
VERSION = '0.1'
AUTHOR = 'Saurav Pandey'
AUTHOR_EMAIL = 'pandeysaurav878@gmail.com'
DESCRIPTION = 'A Python package for various number-related operations.'
URL = 'https://github.com/Saurav-TB-Pandey/sinum-package'
LICENSE = 'MIT'
KEYWORDS = 'sinum'

# Read the contents of the README file
with open('README.md', 'r', encoding='utf-8') as readme_file:
    long_description = readme_file.read()

# Setup configuration
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,  # Added long description here
    long_description_content_type='text/markdown',  # Specify the content type of the long description
    url=URL,
    license=LICENSE,
    keywords=KEYWORDS,
    packages=find_packages(),
    python_requires='>=3.6',
)