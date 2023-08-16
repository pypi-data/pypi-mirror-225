import os
from setuptools import setup, find_packages

VERSION = '3.0.3.2'

setup(
    name="lexisnexisapi",
    version= VERSION,
    license='MIT',
    author="Robert Cuffney",
    author_email='robert.cuffney@lexisnexis.com',
    description = 'a module to support lexisnexis api(s)',
    long_description = 'see README.md file',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    url='https://pypi.org/project/lexisnexisapi/',
    keywords='metabase webservices lexisnexis',
    install_requires=['pandas','requests','xmltodict',],
)
