# -*- coding: UTF-8 -*-

'''
Module
    file_descriptor_test.py
Copyright
    Copyright (C) 2021 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
    codecipher is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    codecipher is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Defines class FileDescriptorTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of FileDescriptor.
Execute
    python3 -m unittest -v file_descriptor_test
'''

import sys
import unittest
from typing import List

try:
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from daemonpy.file_descriptor import FileDescriptor
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '1.8.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileDescriptorTestCase(unittest.TestCase):
    '''
        Defines class FileDescriptorTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of FileDescriptor.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test cases.
                | tearDown - Call after test cases.
                | test_creation - Test creation.
                | test_cration_none_path - Test creation None path.
                | test_cration_empty_path - Test creation empty path.
                | test_cration_none_mode - Test creation None mode.
                | test_cration_empty_mode - Test creation empty mode.
    '''

    def setUp(self) -> None:
        '''Call before test cases.'''

    def tearDown(self) -> None:
        '''Call after test cases.'''

    def test_creation(self) -> None:
        '''Test creation.'''
        null: str = '/dev/null'
        with FileDescriptor(
            null, FileDescriptor.FORMAT[FileDescriptor.STDIN]
        ) as in_file:
            self.assertIsNotNone(in_file)

    def test_creation_none_path(self) -> None:
        '''Test creation None path.'''
        with self.assertRaises(ATSTypeError):
            with FileDescriptor(
                None, FileDescriptor.FORMAT[FileDescriptor.STDIN]
            ):
                print('Not reachable')

    def test_creation_empty_path(self) -> None:
        '''Test creation empty path.'''
        with self.assertRaises(ATSValueError):
            with FileDescriptor(
                '', FileDescriptor.FORMAT[FileDescriptor.STDIN]
            ):
                print('Not reachable')

    def test_creation_none_mode(self) -> None:
        '''Test creation None mode.'''
        null: str = '/dev/null'
        with self.assertRaises(ATSValueError):
            with FileDescriptor(null, None):
                print('Not reachable')

    def test_creation_empty_mode(self) -> None:
        '''Test creation empty mode.'''
        null: str = '/dev/null'
        with self.assertRaises(ATSValueError):
            with FileDescriptor(null, ''):
                print('Not reachable')


if __name__ == '__main__':
    unittest.main()
