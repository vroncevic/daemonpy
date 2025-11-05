# -*- coding: UTF-8 -*-

'''
Module
    file_descriptor.py
Copyright
    Copyright (C) 2020 - 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
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
    Defines class FileDescriptor with attribute(s) and method(s).
    Creates an API for the file descriptor context management.
'''

import sys
from typing import Any, List, Dict, IO, Optional

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:  # pragma: no cover
    # Force exit python #######################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')  # pragma: no cover

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__: str = '2.0.7'
__maintainer__: str = 'Vladimir Roncevic'
__email__: str = 'elektron.ronca@gmail.com'
__status__: str = 'Updated'


class FileDescriptor:
    '''
        Defines class FileDescriptor with attribute(s) and method(s).
        Creates an API for the file descriptor context management.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | STDIN - Standard input is a stream id for input data.
                | STDOUT - Standard output is a stream id for output data.
                | STDERR - Standard error is a stream id for error messages.
                | FORMAT - Supported desciptor types with modes.
                | _desc_path - File descriptor device path.
                | _desc_type - File descriptor device type.
                | _desc_file - File descriptor device object.
            :methods:
                | __init__ - Initials FileDescriptor constructor.
                | __enter__ - Opens descriptor file.
                | __exit__  - Closes descriptor file.
    '''

    _P_VERBOSE: str = 'DAEMONPY::FILE_DESCRIPTOR'
    STDIN: int = 0
    STDOUT: int = 1
    STDERR: int = 2
    FORMAT: Dict[int, Any] = {
        STDIN: 'r', STDOUT: 'a+', STDERR: ['a+', 0]
    }

    def __init__(self, desc_path: str, desc_type: Any) -> None:
        '''
            Initials FileDescriptor constructor.

            :param desc_path: file descriptor device path
            :type desc_path: <str>
            :param desc_type: file descriptor device type
            :type desc_type: <int>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:desc_path', desc_path)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(desc_path):
            raise ATSValueError('missing device path file')
        if any([not bool(desc_type), desc_type not in self.FORMAT.values()]):
            raise ATSValueError('check device file format')
        self._desc_path: Optional[str] = desc_path
        self._desc_type: str | List[str | int] = desc_type
        self._desc_file: Optional[IO[Any]] = None

    def __enter__(self) -> IO[Any] | None:
        '''
            Opens descriptor file.

            :return: File IO stream | None
            :rtype: <IO[Any]> | <NoneType>
            :exceptions: None
        '''
        if bool(self._desc_path) and bool(self._desc_type):
            if isinstance(self._desc_type, str):
                self._desc_file = open(
                    self._desc_path, self._desc_type, encoding='utf-8'
                )
            else:
                if isinstance(self._desc_type[0], str):
                    if isinstance(self._desc_type[1], int):
                        if self._desc_type[1] == 0:
                            self._desc_file = open(
                                self._desc_path,
                                self._desc_type[0],
                                self._desc_type[1],
                                encoding='utf-8'
                            )
        return self._desc_file

    def __exit__(self, *args: Any) -> None:
        '''
            Closes descriptor file.

            :exceptions: None
        '''
        if bool(self._desc_file):
            if not self._desc_file.closed:
                self._desc_file.close()
