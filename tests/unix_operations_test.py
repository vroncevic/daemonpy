# -*- coding: UTF-8 -*-

'''
Module
    unix_operations_test.py
Copyright
    Copyright (C) 2020 - 2025 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class UnixOperationsTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of UnixOperations.
Execute
    python3 -m unittest -v unix_operations_test
'''

import sys
import unittest
from typing import List

try:
    from daemonpy.unix_operations import UnixOperations
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2025, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__: str = '2.0.6'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class UnixOperationsTestCase(unittest.TestCase):
    '''
        Defines class UnixOperationsTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of UnixOperations.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test cases.
                | tearDown - Call after test cases.
                | test_creation - Test creation.
                | test_default_status - Test default status.
                | test_change_status - Test change status.
    '''

    def setUp(self) -> None:
        '''Call before test case.'''

    def tearDown(self) -> None:
        '''Call after test case.'''

    def test_creation(self) -> None:
        '''Test creation.'''
        unix_op: UnixOperations = UnixOperations()
        self.assertIsNotNone(unix_op)

    def test_default_status(self) -> None:
        '''Test default status.'''
        unix_op: UnixOperations = UnixOperations()
        self.assertTrue(unix_op.unix_status)

    def test_change_status(self) -> None:
        '''Test change status.'''
        unix_op: UnixOperations = UnixOperations()
        unix_op.unix_status = False
        self.assertFalse(unix_op.unix_status)


if __name__ == '__main__':
    unittest.main()
