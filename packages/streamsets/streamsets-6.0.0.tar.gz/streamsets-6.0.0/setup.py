#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 StreamSets, Inc.

"""The setup script."""

import os
from setuptools import setup

requirements = [
    'dpath==1.5.0',
    'inflection',
    'PyYAML',
    'requests'
]

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'streamsets', 'sdk', '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name='streamsets',
    version=about['__version__'],
    description='A Python SDK for StreamSets',
    author='StreamSets Inc.',
    packages=['streamsets.sdk'],
    include_package_data=True,
    install_requires=requirements,
    dependency_links=['https://github.com/streamsets/dpath-python/tarball/master#egg=dpath-1.4.2'],
    python_requires='>=3',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ]
)
