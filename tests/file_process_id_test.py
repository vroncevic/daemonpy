#!/usr/bin/env python

'''
 Module
     file_descriptor_test.py
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
     Defined class FileProcessIdTestCase with attribute(s) and method(s).
     Created test cases for checking functionalities of FileProcessId.
 Execute
     python -m unittest -v file_descriptor_test
'''

import sys
import unittest
from datetime import datetime

try:
    from daemonpy.file_process_id import FileProcessId
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


class FileProcessIdTestCase(unittest.TestCase):
    '''
        Defined class FileProcessIdTestCase with attribute(s) and method(s).
        Created test cases for checking functionalities of FileProcessId.
        It defines:

            :attributes:
                | daemon_process_id - file for IO operation.
            :methods:
                | setUp - call before test cases.
                | tearDown - call after test cases.
                | test_file_descriptor_mode_write - test file process id write check.
                | test_file_descriptor_mode_read - test file process id read check.
                | test_file_descriptor - test file process id check.
    '''

    def setUp(self):
        '''Call before test cases.'''
        self.daemon_process_id = 'simple_process_id.txt'

    def tearDown(self):
        '''Call after test cases.'''
        self.daemon_process_id = None

    def test_file_descriptor_mode_write(self):
        '''Test file process id write check.'''
        self.assertEqual(FileProcessId.MODE[0], 'w+')

    def test_file_descriptor_mode_read(self):
        '''Test file process id read check.'''
        self.assertEqual(FileProcessId.MODE[1], 'r')

    def test_file_descriptor(self):
        '''Test file process id check.'''
        with FileProcessId(self.daemon_process_id, 'w+') as daemon_process_id:
            date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            daemon_process_id.write(date)
            self.assertEqual(daemon_process_id is not None, True)


if __name__ == '__main__':
    unittest.main()
