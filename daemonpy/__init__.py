# -*- coding: UTF-8 -*-

'''
Module
    __init__.py
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
    Defines class Daemon with attribute(s) and method(s).
    Creates a base class with backend API.
'''

import sys
from typing import List
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
except ImportError as ats_error_message:
    # Force close python ATS ##################################################
    sys.exit(f'\n{__file__}\n{ats_error_message}\n')

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2024, https://vroncevic.github.io/daemonpy'
__credits__: List[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/dev/LICENSE'
__version__ = '1.8.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Daemon(UnixOperations):
    '''
        Defines class Daemon with attribute(s) and method(s).
        Creates a base class with backend API.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | _daemon_usage - Daemon usage.
                | _pid_path - PID file path.
            :methods:
                | __init__ - Initials Daemon constructor.
                | daemonize - Creates daemon process.
                | start - Starts daemon process.
                | stop - Stops daemon process.
                | restart - Restarts daemon process.
                | exit_handler - At exit delete PID file.
                | run - Runs daemon process (abstract method).
    '''

    _PKG_VERBOSE: str = 'DAEMONPY'

    def __init__(self, pid_path: str, verbose: bool = False) -> None:
        '''
            Initials Daemon constructor.

            :param pid_path: PID file path
            :type pid_path: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        super().__init__()
        error_msg: str | None = None
        error_id: int | None = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:pid_path', pid_path)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(pid_path):
            raise ATSValueError('missing PID file')
        verbose_message(verbose, [f'{self._PKG_VERBOSE} init daemon process'])
        self._daemon_usage: DaemonUsage | None = None
        self._pid_path: str | None = None
        if self.unix_status:
            self._daemon_usage = DaemonUsage()
            self._pid_path = pid_path

    def usage(self, operation: str, verbose: bool = False) -> None:
        '''
            Creates daemon process.

            :param operation: Daemon operation
            :type operation: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:operation', operation)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(operation):
            raise ATSValueError('missing operation')
        verbose_message(
            verbose, [f'{self._PKG_VERBOSE} daemon operation', operation]
        )
        if self.unix_status:
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
                error_message([f'{self._PKG_VERBOSE} wrong option code'])
                sys.exit(128)

    def daemonize(self, verbose: bool = False) -> None:
        '''
            Creates daemon process.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        null: str = '/dev/null'
        verbose_message(
            verbose, [f'{self._PKG_VERBOSE} create daemon process']
        )
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
                dup2(in_file.fileno(), sys.stdin.fileno())
            with FileDescriptor(null, FileDescriptor.STDOUT) as out_file:
                dup2(out_file.fileno(), sys.stdout.fileno())
            with FileDescriptor(null, FileDescriptor.STDERR) as err_file:
                dup2(err_file.fileno(), sys.stderr.fileno())
            register(self.exit_handler)
            with FileProcessId(self._pid_path, 'w+') as pid_path:
                pid_path.write(f'{str(getpid())}\n')

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
        verbose_message(
            verbose, [f'{self._PKG_VERBOSE} start daemon process']
        )
        if self.unix_status:
            with FileProcessId(self._pid_path, 'w+') as pid_path:
                if bool(pid_path.read().strip()):
                    error_message([
                        f'{self._PKG_VERBOSE} file',
                        self._pid_path,
                        'already exist daemon already running?'
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
        verbose_message(
            verbose, [f'{self._PKG_VERBOSE} stop daemon process']
        )
        if self.unix_status:
            with FileProcessId(self._pid_path, 'r') as pid_path:
                pid: int = int(pid_path.read().strip())
                if not pid:
                    error_message(
                        [f'{self._PKG_VERBOSE} daemon process running?']
                    )
                else:
                    status = self.unix_kill(pid, self._pid_path)
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
        verbose_message(
            verbose, [f'{self._PKG_VERBOSE} restart daemon process']
        )
        if self.unix_status:
            if all([self.stop(verbose), self.start(verbose)]):
                status = True
            else:
                error_message(
                    [f'{self._PKG_VERBOSE} faled to restart daemon process']
                )
        else:
            error_message(
                [f'{self._PKG_VERBOSE} daemon process is active?']
            )
        return status

    def exit_handler(self, verbose: bool = False) -> None:
        '''
            Remove PID file at exit.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        if self.unix_status:
            if exists(self._pid_path):
                verbose_message(
                    verbose, [
                        f'{self._PKG_VERBOSE} removing pid file',
                        self._pid_path
                    ]
                )
                remove(self._pid_path)
            else:
                error_message(
                    [
                        f'{self._PKG_VERBOSE} check PID file',
                        self._pid_path
                    ]
                )

    @abstractmethod
    def run(self):
        '''
            Run daemon process.
            Override this method when subclass self.
            It will be called after the process has been
            daemonized by start() or restart().

            :exceptions: None
        '''
