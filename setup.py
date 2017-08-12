#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2015-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import runpy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = "milestonemaker"

metadata_filename = "{}/metadata.py".format(package_name)
metadata = runpy.run_path(metadata_filename)

# http://pypi.python.org/pypi?:action=list_classifiers
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Bug Tracking",
    "Topic :: Software Development :: Libraries",
    "Topic :: Utilities",
]

setup(
    name=package_name,
    version=metadata['__version__'],
    license=metadata['__license__'],
    classifiers=classifiers,
    description="Create milestones in GitHub automatically",
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    url="http://lionheartsw.com/",
    packages=[package_name],
    scripts=['bin/milestonemaker'],
)

