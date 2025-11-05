# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
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
    Defines class Daemon with attribute(s) and method(s).
    Creates a base class with backend API.
'''

import sys
from typing import List, Optional
from atexit import register
from os.path import exists
from os import chdir, setsid, umask, dup2, getpid, remove
from abc import abstractmethod

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_value_error import ATSValueError
    from daemonpy.daemon_usage import DaemonUsage
    from daemonpy.file_process_id import FileProcessId
    from daemonpy.file_descriptor import FileDescriptor
    from daemonpy.unix_operations import UnixOperations
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


class Daemon(UnixOperations):
    '''
        Defines class Daemon with attribute(s) and method(s).
        Creates a base class with backend API.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | _daemon_usage - Daemon usage.
                | _pid - PID file path.
            :methods:
                | __init__ - Initials Daemon constructor.
                | daemonize - Creates daemon process.
                | start - Starts daemon process.
                | stop - Stops daemon process.
                | restart - Restarts daemon process.
                | exit_handler - At exit delete PID file.
                | run - Runs daemon process (abstract method).
    '''

    _P_VERBOSE: str = 'DAEMONPY'

    def __init__(self, pid: str, verbose: bool = False) -> None:
        '''
            Initials Daemon constructor.

            :param pid: PID file path
            :type pid: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        super().__init__()
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([('str:pid', pid)])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pid):
            raise ATSValueError('missing PID file')
        verbose_message(verbose, [f'{self._P_VERBOSE} init daemon'])
        self._daemon_usage: Optional[DaemonUsage] = None
        self._pid: Optional[str] = None
        if self.unix_status:
            self._daemon_usage = DaemonUsage()
            self._pid = pid

    def usage(self, operation: str, verbose: bool = False) -> None:
        '''
            Creates daemon process.

            :param operation: Daemon operation
            :type operation: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: Optional[str] = None
        error_id: Optional[int] = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:operation', operation)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(operation):
            raise ATSValueError('missing daemon operation')
        verbose_message(verbose, [f'{self._P_VERBOSE} daemon', operation])
        if self.unix_status and bool(self._daemon_usage):
            self._daemon_usage.check(operation, verbose)
            if self._daemon_usage.usage_status == 127:
                sys.exit(127)
            elif self._daemon_usage.usage_status == 0:
                self.start(verbose)
            elif self._daemon_usage.usage_status == 1:
                self.stop(verbose)
            elif self._daemon_usage.usage_status == 2:
                self.restart(verbose)
            else:
                error_message([f'{self._P_VERBOSE} wrong option code'])
                sys.exit(128)

    def daemonize(self, verbose: bool = False) -> None:
        '''
            Creates daemon process.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        null: str = '/dev/null'
        verbose_message(verbose, [f'{self._P_VERBOSE} create daemon'])
        if self.unix_status:
            try:
                self.first_fork()
                chdir('/')
                setsid()
                umask(0)
                self.second_fork()
            except OSError as os_error:
                error_message([
                    f'fork #1 failed: {os_error.errno} {os_error.strerror}\n'
                ])
                sys.exit(1)
            sys.stdout.flush()
            sys.stderr.flush()
            with FileDescriptor(null, FileDescriptor.STDIN) as in_file:
                if bool(in_file):
                    dup2(in_file.fileno(), sys.stdin.fileno())
            with FileDescriptor(null, FileDescriptor.STDOUT) as out_file:
                if bool(out_file):
                    dup2(out_file.fileno(), sys.stdout.fileno())
            with FileDescriptor(null, FileDescriptor.STDERR) as err_file:
                if bool(err_file):
                    dup2(err_file.fileno(), sys.stderr.fileno())
            register(self.exit_handler)
            with FileProcessId(self._pid, 'w+') as pid:
                if bool(pid):
                    pid.write(f'{str(getpid())}\n')

    def start(self, verbose: bool = False) -> bool:
        '''
            Start daemon process.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        status: bool = False
        verbose_message(verbose, [f'{self._P_VERBOSE} start daemon'])
        if self.unix_status:
            with FileProcessId(self._pid, 'w+') as pid:
                if bool(pid):
                    pid_content: str = pid.read().strip()
                    if bool(pid_content):
                        error_message([
                            f'{self._P_VERBOSE} file', self._pid,
                            'already exists, daemon already running?'
                        ])
                    else:
                        self.daemonize(verbose)
                        self.run()
                        status = True
        return status

    def stop(self, verbose: bool = False) -> bool:
        '''
            Stop daemon process.

            :param verbose: Enable/Disable verbose option.
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        status: bool = False
        verbose_message(verbose, [f'{self._P_VERBOSE} stop daemon'])
        if self.unix_status:
            with FileProcessId(self._pid, 'r') as pid:
                if bool(pid) and bool(self._pid):
                    pid_content: str = pid.read().strip()
                    if not bool(pid_content):
                        error_message([f'{self._P_VERBOSE} daemon running?'])
                    else:
                        status = self.unix_kill(int(pid_content), self._pid)
        return status

    def restart(self, verbose: bool = False) -> bool:
        '''
            Restart daemon process.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :return: True (success operation) | False
            :rtype: <bool>
            :exceptions: None
        '''
        status: bool = False
        verbose_message(verbose, [f'{self._P_VERBOSE} restart daemon'])
        if self.unix_status:
            if all([self.stop(verbose), self.start(verbose)]):
                status = True
            else:
                error_message([f'{self._P_VERBOSE} faled to restart daemon'])
        else:
            error_message([f'{self._P_VERBOSE} daemon is active?'])
        return status

    def exit_handler(self, verbose: bool = False) -> None:
        '''
            Remove PID file at exit.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        if self.unix_status:
            if not bool(self._pid):
                error_message([f'{self._P_VERBOSE} check PID', self._pid])
            else:
                if exists(self._pid):
                    verbose_message(
                        verbose, [f'{self._P_VERBOSE} removing PID', self._pid]
                    )
                    remove(self._pid)
                else:
                    error_message([f'{self._P_VERBOSE} check PID', self._pid])

    @abstractmethod
    def run(self) -> None:
        '''
            Run daemon process.
            Override this method when subclass self.
            It will be called after the process has been
            daemonized by start() or restart().

            :exceptions: None
        '''
