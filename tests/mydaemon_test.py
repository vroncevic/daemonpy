#!/usr/bin/env python

'''
 Module
     mydaemon.py
 Copyright
     Copyright (C) 2022 Vladimir Roncevic <elektron.ronca@gmail.com>
     mydaemon is free software: you can redistribute it and/or modify it
     under the terms of the GNU General Public License as published by the
     Free Software Foundation, either version 3 of the License, or
     (at your option) any later version.
     mydaemon is distributed in the hope that it will be useful, but
     WITHOUT ANY WARRANTY; without even the implied warranty of
     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
     See the GNU General Public License for more details.
     You should have received a copy of the GNU General Public License along
     with this program. If not, see <http://www.gnu.org/licenses/>.
 Info
     Defined class ATSAbstractTestCase with attribute(s) and method(s).
     Created test cases for checking functionalities of AbstractMethod.
 Execute
     python -m unittest -v mydaemon_test
'''

import sys
import unittest
from time import sleep

try:
    from daemonpy import Daemon
except ImportError as ats_error:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error)
    sys.exit(MESSAGE)  # Force close python ATS ##############################


class MyDaemon(Daemon):
    '''Simple Daemon Class with sleep operation'''

    def run(self):
        '''
            Run Daemon process with time sleep example.

            :exceptions: None
        '''
        while True:
            sleep(1)


class MyDaemonTestCase(unittest.TestCase):
    '''
        Defined class MyDaemonTestCase with attribute(s) and method(s).
        Created test cases for checking functionalities of MyDaemon.
        It defines:

            :attributes:
                | None
            :methods:
                | setUp - call before test cases.
                | tearDown - call after test cases.
                | test_daemon_usage - test for base usage of daemonpy.
    '''

    def setUp(self):
        '''Call before test cases.'''
        self.daemon = MyDaemon('/tmp/daemon-example.pid')

    def tearDown(self):
        '''Call after test cases.'''
        self.daemon = None

    def test_daemon_usage(self):
        '''Test base encoding.'''
        with self.assertRaises(SystemExit):
            self.daemon.usage('start')
            sleep(5)
            self.daemon.usage('stop')


if __name__ == '__main__':
    unittest.main()
