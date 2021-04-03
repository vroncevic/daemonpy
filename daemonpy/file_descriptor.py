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
__license__ = 'https://github.com/vroncevic/daemonpy/blob/master/LICENSE'
__version__ = '1.5.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileDescriptor(object):
    '''
        Defined class FileDescriptor with attribute(s) and method(s).
        Created API for file descriptor context management.
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | STDIN - Standard input is a stream id for input data.
                | STDOUT - Standard output is a stream id for output data.
                | STDERR - Standard error is a stream id for error messages.
                | FORMAT - Supported desciptor types with modes.
                | __device_path - File descriptor device path.
                | __device_type - File descriptor device type.
                | __device_file - File descriptor device object.
            :methods:
                | __init__ - Initial constructor.
                | __enter__ - Open descriptor file.
                | __exit__  - Close descriptor file.
                | __str__ - Dunder method for object FileDescriptor.
    '''

    __slots__ = (
        'VERBOSE', 'STDIN', 'STDOUT', 'STDERR', 'FORMAT',
        '__device_path', '__device_type', '__device_file'
    )
    VERBOSE = 'DAEMONPY::FILE_DESCRIPTOR'
    STDIN, STDOUT, STDERR = 0, 1, 2
    FORMAT = {
        STDIN: 'r', STDOUT: 'a+', STDERR: ['a+', 0]
    }

    def __init__(self, device_path, device_type):
        '''
            Initial constructor.

            :param device_path: File descriptor device path.
            :type device_path: <str>
            :param device_type: File descriptor device type.
            :type device_type: <int>
            :param verbose: Enable/disable verbose option.
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
            error_message(FileDescriptor.VERBOSE, error)

    def __enter__(self):
        '''
            Open descriptor file.

            :return: File Device object | None.
            :rtype: <file> | <NoneType>
            :exceptions: ATSParameterError
        '''
        error = None
        file_descriptor_mode = FileDescriptor.FORMAT[self.__device_type]
        if isinstance(file_descriptor_mode, str):
            self.__device_file = open(
                self.__device_path, file_descriptor_mode
            )
        elif isinstance(file_descriptor_mode, list):
            if len(file_descriptor_mode) == 2:
                check_file_descriptor_mode_ok = all([
                    isinstance(file_descriptor_mode[0], str),
                    isinstance(file_descriptor_mode[1], int),
                    file_descriptor_mode[1] == 0
                ])
                if check_file_descriptor_mode_ok:
                    self.__device_file = open(
                        self.__device_path,
                        file_descriptor_mode[0],
                        file_descriptor_mode[1]
                    )
                else:
                    error = 'check file descriptor mode'
                    raise ATSParameterError(error)
            else:
                error = 'check format of file descriptor mode'
                raise ATSParameterError(error)
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

            :return: Object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2}, {3})'.format(
            self.__class__.__name__, self.__device_path,
            self.__device_type, self.__device_file
        )
