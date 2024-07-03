# -*- coding: UTF-8 -*-

'''
Module
    unix_operations.py
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
    Defines class UnixOperations with attribute(s) and method(s).
    Creates an API for operating Unix Like OS processes.
'''

import sys
from typing import List, Optional
from os import fork, kill, remove
from os.path import exists
from signal import SIGTERM
from time import sleep

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '2.0.5'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class UnixOperations:
    '''
        Defines class UnixOperations with attribute(s) and method(s).
        Creates an API for operating Unix Like OS processes.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | _OS_TARGET - List of supported operating systems.
                | _NO_PROCESS - No such process message.
                | _unix_status - Unix status (True for unix like OS).
            :methods:
                | __init__ - Initials UnixOperations constructor.
                | unix_status - Property methods for set/get operations.
                | first_fork - Makes sure that process is not group leader.
                | second_fork - Won't be started merely by opening a terminal.
                | unix_kill - Kills unix like OS process.
    '''

    _P_VERBOSE: str = 'DAEMONPY::UNIX_OPERATIONS'
    _OS_TARGET: List[str] = ['linux', 'linux2']
    _NO_PROCESS: str = 'No such process'
    _SLEEP: float = 0.1

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials UnixOperations constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(
            verbose, [f'{self._P_VERBOSE} init daemon operations']
        )
        self._unix_status: bool = any(
            sys.platform == os_target for os_target in self._OS_TARGET
        )

    @property
    def unix_status(self) -> bool:
        '''
            Property method for getting unix like OS status.

            :return: Unix like OS status
            :rtype: <bool>
            :exceptions: None
        '''
        return self._unix_status

    @unix_status.setter
    def unix_status(self, unix_status: bool) -> None:
        '''
            Property method for setting unix like OS status.

            :param unix_status: Unix like OS status
            :type unix_status: <bool>
            :exceptions: None
        '''
        self._unix_status = unix_status

    def first_fork(self, verbose: bool = False) -> None:
        '''
            Makes sure that process is not group leader.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exit code: 0 (success fork) | 1 (failed)
            :exceptions: None
        '''
        if self._unix_status:
            if fork() > 0:
                verbose_message(verbose, [f'{self._P_VERBOSE} first fork'])
                sys.exit(0)

    def second_fork(self, verbose: bool = False) -> None:
        '''
            Won't be started merely by opening a terminal.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exit code: 0 (success fork) | 1 (failed)
            :exceptions: None
        '''
        if self._unix_status:
            if fork() > 0:
                verbose_message(verbose, [f'{self._P_VERBOSE} second fork'])
                sys.exit(0)

    def unix_kill(
        self, pid: int, pid_path: str, verbose: bool = False
    ) -> bool:
        '''
            Kills Unix Like OS process.

            :param pid: Process ID
            :type pid: <int>
            :param pid_path: PID file path
            :type pid_path: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('int:pid', pid), ('str:pid_path', pid_path)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pid):
            raise ATSValueError('missing PID')
        if not bool(pid_path):
            raise ATSValueError('missing PID path')
        status: bool = False
        if self._unix_status:
            try:
                verbose_message(
                    verbose, [f'{self._P_VERBOSE} kill process {pid}']
                )
                while True:
                    kill(pid, SIGTERM)
                    sleep(self._SLEEP)
                    status = True
            except OSError as os_error:
                os_error = str(os_error)
                if os_error.find(self._NO_PROCESS) > 0:
                    if exists(pid_path):
                        verbose_message(
                            verbose,
                            [
                                f'{self._P_VERBOSE}',
                                f'{self._NO_PROCESS}',
                                f'with PID: {pid},',
                                f'removing pid file {pid_path}'
                            ]
                        )
                        remove(pid_path)
                        status = True
                else:
                    error_message([f'{self._P_VERBOSE} {os_error}'])
        return status
