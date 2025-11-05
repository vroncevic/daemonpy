# -*- coding: UTF-8 -*-

'''
Module
    file_process_id.py
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
    Defines class FileProcessId with attribute(s) and method(s).
    Creates an API for the file process id context management.
'''

import sys
from typing import Any, List, IO, Optional

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


class FileProcessId:
    '''
        Defines class FileProcessId with attribute(s) and method(s).
        Creates an API for the file process id context management.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | _MODE - Supported modes for process id file.
                | _pid_path - PID file path.
                | _pid_mode - PID file mode.
                | _pid - PID file object.
            :methods:
                | __init__ - Initials FileProcessId constructor.
                | __enter__ - Opens PID file.
                | __exit__ - Closes PID file.
    '''

    _P_VERBOSE: str = 'DAEMONPY::FILE_PROCESS_ID'
    _MODE: List[str] = ['w+', 'r']

    def __init__(
        self, pid_path: Optional[str], pid_mode: Optional[str]
    ) -> None:
        '''
            Initials FileProcessId constructor.

            :param pid_path: file process id path | None
            :type pid_path: <Optional[str]>
            :param pid_mode: file process id mode | None
            :type pid_mode: <Optional[str]>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:pid_path', pid_path), ('str:pid_mode', pid_mode)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pid_path):
            raise ATSValueError('missing PID path file')
        if any([not bool(pid_mode), pid_mode not in self._MODE]):
            raise ATSValueError('check PID mode file')
        self._pid_path: Optional[str] = pid_path
        self._pid_mode: Optional[str] = pid_mode
        self._pid: Optional[IO[Any]] = None

    def __enter__(self) -> Optional[IO[Any]]:
        '''
            Opens PID file.

            :return: File IO stream | None
            :rtype: <Optional[IO[Any]]>
            :exceptions: None
        '''
        if bool(self._pid_path) and bool(self._pid_mode):
            self._pid = open(
                self._pid_path, self._pid_mode, encoding='utf-8'
            )
        return self._pid

    def __exit__(self, *args: Any) -> None:
        '''
            Closes PID file.

            :exceptions: None
        '''
        if bool(self._pid):
            if not self._pid.closed:
                self._pid.close()
