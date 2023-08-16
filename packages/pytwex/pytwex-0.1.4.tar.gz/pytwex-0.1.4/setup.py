from io import open
from setuptools import setup
from pathlib import Path

"""
:authors: flexter1
:copyright: (c) 2023 flexter1
"""

version = '0.1.4'

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pytwex',
    version=version,

    author='flexter1',

    description=(u'Python asynchronous module for interacting with Twitter using auth_token for Python 3.10+'),
    long_description=long_description,
    long_description_content_type='text/markdown',


    packages=['pytwex'],
    install_requires=['loguru~=0.7.0', 'aiohttp~=3.8.4', 'pyuseragents~=1.0.5', 'requests~=2.31.0'],

)
