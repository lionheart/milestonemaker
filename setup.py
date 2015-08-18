#!/usr/bin/env python

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata = {}
execfile("milestonemaker/metadata.py", metadata)

setup(
    name='milestonemaker',
    version=metadata['__version__'],
    license=metadata['__license__'],
    description="Create milestones in GitHub automatically",
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url="http://lionheartsw.com/",
    packages=[
        'milestonemaker',
    ],
    scripts=[
        'bin/milestonemaker',
    ],
)

