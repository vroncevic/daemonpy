# -*- coding: UTF-8 -*-

'''
Module
    daemon_usage_test.py
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
    Defines class DaemonUsageTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of DaemonUsage.
Execute
    python3 -m unittest -v daemon_usage_test
'''

import sys
import unittest
from typing import List

try:
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from daemonpy.daemon_usage import DaemonUsage
except ImportError as test_error_message:
    # Force close python test #################################################
    sys.exit(f'\n{__file__}\n{test_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '2.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DaemonUsageTestCase(unittest.TestCase):
    '''
        Defines class DaemonUsageTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of DaemonUsage.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test cases.
                | tearDown - Call after test cases.
                | test_create - Test creation of daemon usage.
                | test_default_status - Test default daemon usage status.
                | test_change_status - Test changes of daemon usage status.
                | test_usage - Test daemon usage start.
                | test_usage_none - Test None usage.
                | test_usage_empty - Test empty usage.
    '''

    def setUp(self) -> None:
        '''Call before test cases.'''

    def tearDown(self) -> None:
        '''Call after test cases.'''

    def test_create(self) -> None:
        '''Test creation of daemon usage.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        self.assertIsNotNone(daemon_usage)

    def test_default_status(self) -> None:
        '''Test default daemon usage status.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        self.assertEqual(daemon_usage.usage_status, 0)

    def test_change_status(self) -> None:
        '''Test changes of daemon usage status.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        daemon_usage.usage_status = 0
        daemon_usage.usage_status = 1
        daemon_usage.usage_status = 0
        self.assertEqual(daemon_usage.usage_status, 0)

    def test_usage(self) -> None:
        '''Test daemon usage start.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        daemon_usage.check('start')
        self.assertEqual(daemon_usage.usage_status, 0)

    def test_usage_none(self) -> None:
        '''Test None usage.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        with self.assertRaises(ATSTypeError):
            daemon_usage.check(None)  # type: ignore

    def test_usage_empty(self) -> None:
        '''Test empty usage.'''
        daemon_usage: DaemonUsage = DaemonUsage()
        with self.assertRaises(ATSValueError):
            daemon_usage.check('')


if __name__ == '__main__':
    unittest.main()
