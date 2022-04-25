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
     Defined class FileDescriptorTestCase with attribute(s) and method(s).
     Created test cases for checking functionalities of FileDescriptor.
 Execute
     python -m unittest -v file_descriptor_test
'''

import sys
import unittest
from datetime import datetime

try:
    from daemonpy.file_descriptor import FileDescriptor
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


class FileDescriptorTestCase(unittest.TestCase):
    '''
        Defined class FileDescriptorTestCase with attribute(s) and method(s).
        Created test cases for checking functionalities of FileDescriptor.
        It defines:

            :attributes:
                | daemon_file_name - file for IO operation.
            :methods:
                | setUp - call before test cases.
                | tearDown - call after test cases.
                | test_file_descriptor_stdin - test file descriptor stdin check.
                | test_file_descriptor_stdout - test file descriptor stdout check.
                | test_file_descriptor_stderr - test file descriptor stderr check.
                | test_file_descriptor - test file descriptor check.
    '''

    def setUp(self):
        '''Call before test cases.'''
        self.daemon_file_name = 'simple_test.txt'

    def tearDown(self):
        '''Call after test cases.'''
        self.daemon_file_name = None

    def test_file_descriptor_stdin(self):
        '''Test file descriptor stdin check.'''
        self.assertEqual(FileDescriptor.STDIN, 0)

    def test_file_descriptor_stdout(self):
        '''Test file descriptor stdout check.'''
        self.assertEqual(FileDescriptor.STDOUT, 1)

    def test_file_descriptor_stderr(self):
        '''Test file descriptor stderr check.'''
        self.assertEqual(FileDescriptor.STDERR, 2)

    def test_file_descriptor(self):
        '''Test file descriptor check.'''
        with FileDescriptor(
            self.daemon_file_name, FileDescriptor.STDOUT
        ) as simple_test:
            date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            simple_test.write(date)
            self.assertEqual(simple_test is not None, True)


if __name__ == '__main__':
    unittest.main()
