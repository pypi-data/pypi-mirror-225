#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import io
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext
from pathlib import Path

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='puid-py',
    version='1.2.0',
    license='MIT',
    description='Simple, flexible and efficient generation of probably unique identifiers (`puid`, '
    'aka random strings) of intuitively specified entropy using pre-defined or custom characters, '
    'including unicode',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Paul Rogers',
    author_email='paul@dingosky.com',
    url='https://github.com/puid/python',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
    project_urls={
        'Documentation': 'https://puid-py.readthedocs.io/',
        'Changelog': 'https://puid-py.readthedocs.io/en/latest/changelog.html',
        'Issue Tracker': 'https://github.com/puid/python/issues',
    },
    keywords=['random string', 'random ID', 'uuid', 'secure token', 'security', 'token'],
    python_requires='>=3.7',
    install_requires=[
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={
        'console_scripts': [
            'puid = puid.cli:main',
        ]
    },
)
