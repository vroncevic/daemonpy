# -*- coding: UTF-8 -*-

'''
 Module
     file_descriptor.py
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
     Defined class FileDescriptor with attribute(s) and method(s).
     Created API for file descriptor context management.
'''

import sys

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
    from ats_utilities.exceptions.ats_parameter_error import ATSParameterError
except ImportError as ats_error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error_message)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '1.7.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileDescriptor:
    '''
        Defined class FileDescriptor with attribute(s) and method(s).
        Created API for file descriptor context management.
        It defines:

            :attributes:
                | PKG_VERBOSE - console text indicator for process-phase.
                | STDIN - standard input is a stream id for input data.
                | STDOUT - standard output is a stream id for output data.
                | STDERR - standard error is a stream id for error messages.
                | FORMAT - supported desciptor types with modes.
                | __device_path - file descriptor device path.
                | __device_type - file descriptor device type.
                | __device_file - file descriptor device object.
            :methods:
                | __init__ - initial constructor.
                | __enter__ - open descriptor file.
                | __exit__  - close descriptor file.
                | __str__ - dunder method for object FileDescriptor.
    '''

    PKG_VERBOSE = 'DAEMONPY::FILE_DESCRIPTOR'
    STDIN, STDOUT, STDERR = 0, 1, 2
    FORMAT = {
        STDIN: 'r', STDOUT: 'a+', STDERR: 'a+'
    }

    def __init__(self, device_path, device_type):
        '''
            Initial constructor.

            :param device_path: file descriptor device path.
            :type device_path: <str>
            :param device_type: file descriptor device type.
            :type device_type: <int>
            :param verbose: enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([
            ('str:device_path', device_path),
            ('int:device_type', device_type)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        supported_device_types = [
            FileDescriptor.STDIN, FileDescriptor.STDOUT, FileDescriptor.STDERR
        ]
        if device_type in supported_device_types:
            self.__device_path = device_path
            self.__device_type = device_type
            self.__device_file = None
        else:
            error = 'file descriptor type can be <STDIN | STDOUT | STDERR>'
            error_message(FileDescriptor.PKG_VERBOSE, error)

    def __enter__(self):
        '''
            Open descriptor file.

            :return: file device object | None.
            :rtype: <file> | <NoneType>
            :exceptions: ATSParameterError
        '''
        error = None
        file_descriptor_mode = FileDescriptor.FORMAT[self.__device_type]
        if isinstance(file_descriptor_mode, str):
            self.__device_file = open(
                self.__device_path, file_descriptor_mode
            )
        else:
            error = 'unsupported file descriptor mode'
            raise ATSParameterError(error)
        return self.__device_file

    def __exit__(self, *args):
        '''
            Close descriptor file.

            :exceptions: None
        '''
        try:
            self.__device_file.close()
        except AttributeError:
            pass

    def __str__(self):
        '''
            Dunder method for FileDescriptor.

            :return: object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2}, {3})'.format(
            self.__class__.__name__, self.__device_path,
            self.__device_type, self.__device_file
        )
