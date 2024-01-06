# -*- coding: UTF-8 -*-

'''
Module
    daemon_test.py
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
    Defines class DaemonTestCase with attribute(s) and method(s).
    Creates test cases for checking functionalities of Daemon.
Execute
    python3 -m unittest -v daemon_test
'''

import sys
import unittest
from typing import List
from time import sleep

try:
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from daemonpy import Daemon
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


class MyDaemon(Daemon):
    '''
        Defines class MyDaemon with attribute(s) and method(s).
        Sets an operation for Daemon process.

        It defines:

            :attributes:
                | None
            :methods:
                | run - Runs Daemon process (defined method).
    '''

    def run(self):
        '''
            Runs Daemon process with time sleep example.

            :exceptions: None
        '''
        while True:
            sleep(1)


class DaemonTestCase(unittest.TestCase):
    '''
        Defines class DaemonTestCase with attribute(s) and method(s).
        Creates test cases for checking functionalities of MyDaemon.

        It defines:

            :attributes:
                | None
            :methods:
                | setUp - Call before test cases.
                | tearDown - Call after test cases.
                | test_run_usage_with_none - Test daemon usage with None.
                | test_run_usage_with_empty - Test daemon usage with empty.
    '''

    def setUp(self) -> None:
        '''Call before test cases.'''

    def tearDown(self) -> None:
        '''Call after test cases.'''

    def test_create(self) -> None:
        '''Test creation of daemon.'''
        my_daemon: MyDaemon = MyDaemon('/tmp/daemon-example.pid')
        self.assertIsNotNone(my_daemon)

    def test_run_usage_with_none(self) -> None:
        '''Test daemon usage with None.'''
        my_daemon: MyDaemon = MyDaemon('/tmp/daemon-example.pid')
        with self.assertRaises(ATSTypeError):
            my_daemon.usage(None)

    def test_run_usage_with_empty(self) -> None:
        '''Test daemon usage with empty.'''
        my_daemon: MyDaemon = MyDaemon('/tmp/daemon-example.pid')
        with self.assertRaises(ATSValueError):
            my_daemon.usage('')


if __name__ == '__main__':
    unittest.main()
