#!/usr/bin/env python

'''
 Module
     daemon_usage_test.py
 Copyright
     Copyright (C) 2022 Vladimir Roncevic <elektron.ronca@gmail.com>
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
     Defined class DaemonUsageTestCase with attribute(s) and method(s).
     Created test cases for checking functionalities of DaemonUsage.
 Execute
     python -m unittest -v daemon_usage_test
'''

import sys
import unittest

try:
    from daemonpy.daemon_usage import DaemonUsage
except ImportError as ats_error:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2022, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '1.9.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DaemonUsageTestCase(unittest.TestCase):
    '''
        Defined class DaemonUsageTestCase with attribute(s) and method(s).
        Created test cases for checking functionalities of DaemonUsage.
        It defines:

            :attributes:
                | daemon_usage - Daemon usage object.
            :methods:
                | setUp - call before test cases.
                | tearDown - call after test cases.
                | test_daemon_usage_check_start - test daemon usage check start.
                | test_daemon_usage_check_stop - test daemon usage check stop.
                | test_daemon_usage_check_restart - test daemon usage check restart.
    '''

    def setUp(self):
        '''Call before test cases.'''
        self.daemon_usage = DaemonUsage()

    def tearDown(self):
        '''Call after test cases.'''
        self.daemon_usage = None

    def test_daemon_usage_check_start(self):
        '''Test daemon usage check start.'''
        self.daemon_usage.check('start')
        self.assertEqual(self.daemon_usage.usage_status, 0)

    def test_daemon_usage_check_stop(self):
        '''Test daemon usage check stop.'''
        self.daemon_usage.check('stop')
        self.assertEqual(self.daemon_usage.usage_status, 1)

    def test_daemon_usage_check_restart(self):
        '''Test daemon usage check restart.'''
        self.daemon_usage.check('restart')
        self.assertEqual(self.daemon_usage.usage_status, 2)


if __name__ == '__main__':
    unittest.main()
