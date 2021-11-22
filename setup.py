#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
 Module
     setup.py
 Copyright
     Copyright (C) 2020 Vladimir Roncevic <elektron.ronca@gmail.com>
     daemonpy is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     daemonpy is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Defined setup for daemonpy package.
'''

from os.path import abspath, dirname, join
from setuptools import setup

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '1.7.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'

THIS_DIR, LONG_DESCRIPTION = abspath(dirname(__file__)), None
with open(join(THIS_DIR, 'README.md')) as readme:
    LONG_DESCRIPTION = readme.read()

PROGRAMMING_LANG = 'Programming Language :: Python ::'
VERSIONS = [
    '2.7', '3', '3.1', '3.2', '3.3','3.4', '3.5', '3.6', '3.7', '3.8', '3.9'
]
SUPPORTED_PY_VERSIONS = [
    '{0} {1}'.format(PROGRAMMING_LANG, VERSION) for VERSION in VERSIONS
]

LICENSE_PREFIX = 'License :: OSI Approved ::'
LICENSES = [
    'GNU Lesser General Public License v2 (LGPLv2)',
    'GNU Lesser General Public License v2 or later (LGPLv2+)',
    'GNU Lesser General Public License v3 (LGPLv3)',
    'GNU Lesser General Public License v3 or later (LGPLv3+)',
    'GNU Library or Lesser General Public License (LGPL)'
]
APPROVED_LICENSES = [
    '{0} {1}'.format(LICENSE_PREFIX, LICENSE) for LICENSE in LICENSES
]

PYP_CLASSIFIERS = SUPPORTED_PY_VERSIONS + APPROVED_LICENSES

setup(
    name='daemonpy',
    version='1.7.2',
    description='Creating Daemon process',
    author='Vladimir Roncevic',
    author_email='elektron.ronca@gmail.com',
    url='https://vroncevic.github.io/daemonpy/',
    license='GPL 2020 Free software to use and distributed it.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    keywords='Unix, Linux, Daemon, Process',
    platforms='any',
    classifiers=PYP_CLASSIFIERS,
    packages=['daemonpy',],
    install_requires=['ats-utilities',]
)
