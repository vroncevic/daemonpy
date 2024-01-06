# -*- coding: UTF-8 -*-

'''
Module
    file_process_id_test.py
Copyright
    Copyright (C) 2020 - 2024 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class FileProcessIdTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of FileProcessId.
Execute
    python3 -m unittest -v file_process_id_test
'''

import sys
import unittest
from typing import List

try:
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from daemonpy.file_process_id import FileProcessId
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '2.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileProcessIdTestCase(unittest.TestCase):
    '''
        Defines class FileProcessIdTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of FileProcessId.

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
        '''Call before test case.'''

    def tearDown(self) -> None:
        '''Call after test case.'''

    def test_creation(self) -> None:
        '''Test creation.'''
        null: str = '/dev/null'
        with FileProcessId(null, 'w+') as in_file:
            self.assertIsNotNone(in_file)

    def test_cration_none_path(self) -> None:
        '''Test creation None path.'''
        with self.assertRaises(ATSTypeError):
            with FileProcessId(None, 'w+'):
                print('Not reachable')

    def test_cration_empty_path(self) -> None:
        '''Test creation empty path.'''
        with self.assertRaises(ATSValueError):
            with FileProcessId('', 'w+'):
                print('Not reachable')

    def test_cration_none_mode(self) -> None:
        '''Test creation None mode.'''
        null: str = '/dev/null'
        with self.assertRaises(ATSTypeError):
            with FileProcessId(null, None):
                print('Not reachable')

    def test_cration_empty_mode(self) -> None:
        '''Test creation empty mode.'''
        null: str = '/dev/null'
        with self.assertRaises(ATSValueError):
            with FileProcessId(null, ''):
                print('Not reachable')


if __name__ == '__main__':
    unittest.main()
