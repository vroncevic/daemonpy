# -*- coding: UTF-8 -*-

'''
 Module
     file_process_id.py
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
     Defined class FileProcessId with attribute(s) and method(s).
     Created API for file process id context management.
'''

import sys
from os.path import exists

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
__version__ = '1.8.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FileProcessId:
    '''
        Defined class FileProcessId with attribute(s) and method(s).
        Created API for file descriptor context management.
        It defines:

            :attributes:
                | PKG_VERBOSE - console text indicator for process-phase.
                | MODE - supported modes for process id file.
                | __file_process_id_path - PID file path.
                | __file_process_id_mode - PID file mode.
                | __file_process_id - PID file object.
            :methods:
                | __init__ - initial constructor.
                | __enter__ - open PID file.
                | __exit__ - close PID file.
                | __str__ - dunder method for object FileDescriptor.
    '''

    PKG_VERBOSE = 'DAEMONPY::FILE_PROCESS_ID'
    MODE = ['w+', 'r']

    def __init__(self, file_process_id_path, file_process_id_mode):
        '''
            Initial constructor.

            :param file_process_id_path: file process id path.
            :type file_process_id_path: <str>
            :param file_process_id_mode: file process id mode.
            :type file_process_id_mode: <str>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([
            ('str:file_process_id_path', file_process_id_path),
            ('str:file_process_id_mode', file_process_id_mode)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        if file_process_id_mode in FileProcessId.MODE:
            self.__file_process_id_path = file_process_id_path
            self.__file_process_id_mode = file_process_id_mode
            self.__file_process_id = None
        else:
            error = 'PID file mode can be <w+ | r>'
            error_message(FileProcessId.PKG_VERBOSE, error)

    def __enter__(self):
        '''
            Open PID file.

            :return: file device object | None.
            :rtype: <file> | <NoneType>
            :exceptions: ATSParameterError
        '''
        error = None
        if self.__file_process_id_mode == FileProcessId.MODE[1]:
            if not exists(self.__file_process_id_path):
                error = 'check PID file path'
                raise ATSParameterError(error)
            else:
                pass
        elif self.__file_process_id_mode == FileProcessId.MODE[0]:
            pass
        else:
            error = 'check PID file mode'
            raise ATSParameterError(error)
        self.__file_process_id = open(
            self.__file_process_id_path, self.__file_process_id_mode
        )
        return self.__file_process_id

    def __exit__(self, *args):
        '''
            Close PID file.

            :exceptions: None
        '''
        try:
            self.__file_process_id.close()
        except AttributeError:
            pass

    def __str__(self):
        '''
            Dunder method for FileProcessId.

            :return: object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2}, {3})'.format(
            self.__class__.__name__, self.__file_process_id_path,
            self.__file_process_id_mode, self.__file_process_id
        )
