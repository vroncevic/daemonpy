# -*- coding: UTF-8 -*-

'''
 Module
     __init__.py
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
     Defined class Daemon with attribute(s) and method(s).
     Created base class with backend API.
'''

from sys import exit, stdin, stdout, stderr
from atexit import register
from os.path import exists
from os import chdir, setsid, umask, dup2, getpid, remove

try:
    from daemonpy.daemon_usage import DaemonUsage
    from daemonpy.file_process_id import FileProcessId
    from daemonpy.file_descriptor import FileDescriptor
    from daemonpy.unix_operations import UnixOperations
    from ats_utilities.checker import ATSChecker
    from ats_utilities.abstract import abstract_method
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
except ImportError as error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, error_message)
    exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/master/LICENSE'
__version__ = '1.5.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Daemon(UnixOperations):
    '''
        Defined class Daemon with attribute(s) and method(s).
        Created base class with backend API.
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | __daemon_usage - Daemon usage.
                | __pid_file_path - PID file path.
            :methods:
                | __init__ - Initial constructor.
                | daemonize - Create Daemon process.
                | start - Start Daemon process.
                | stop - Stop Daemon process.
                | restart - Restart Daemon process.
                | exit_handler - At exit delete PID file.
                | run - Run Daemon process (abstract method).
    '''

    __slots__ = ('VERBOSE', '__daemon_usage', '__pid_file_path')
    VERBOSE = 'DAEMONPY'

    def __init__(self, pid_file_path, verbose=False):
        '''
            Initial constructor.

            :param pid_file_path: PID file path.
            :type pid_file_path: <str>
            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([
            ('str:pid_file_path', pid_file_path)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        verbose_message(Daemon.VERBOSE, verbose, 'init daemon process')
        UnixOperations.__init__(self)
        if self.unix_status:
            self.__daemon_usage = DaemonUsage()
            self.__pid_file_path = pid_file_path
        else:
            self.__daemon_usage = None
            self.__pid_file_path = None

    def usage(self, operation, verbose=False):
        '''
            Create daemon process.

            :param operation: Daemon operation.
            :type operation: <str>
            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([('str:operation', operation)])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        verbose_message(Daemon.VERBOSE, verbose, 'daemon operation', operation)
        if self.unix_status:
            self.__daemon_usage.check(operation, verbose=verbose)
            if self.__daemon_usage.usage_status == 127:
                exit(127)
            elif self.__daemon_usage.usage_status == 0:
                self.start(verbose=verbose)
            elif self.__daemon_usage.usage_status == 1:
                self.stop(verbose=verbose)
            elif self.__daemon_usage.usage_status == 2:
                self.restart(verbose=verbose)
            else:
                error_message(Daemon.VERBOSE, 'wrong option code')
                exit(128)

    def daemonize(self, verbose=False):
        '''
            Create daemon process.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: None
        '''
        null = '/dev/null'
        verbose_message(Daemon.VERBOSE, verbose, 'create daemon process')
        if self.unix_status:
            self.first_fork()
            chdir('/')
            setsid()
            umask(0)
            self.second_fork()
            stdout.flush()
            stderr.flush()
            with FileDescriptor(null, FileDescriptor.STDIN) as in_file:
                dup2(in_file.fileno(), stdin.fileno())
            with FileDescriptor(null, FileDescriptor.STDOUT) as out_file:
                dup2(out_file.fileno(), stdout.fileno())
            with FileDescriptor(null, FileDescriptor.STDERR) as err_file:
                dup2(err_file.fileno(), stderr.fileno())
            register(self.exit_handler)
            pid = str(getpid())
            with FileProcessId(self.__pid_file_path, 'w+') as pid_file_path:
                pid_file_path.write('{0}\n'.format(pid))

    def start(self, verbose=False):
        '''
            Start Daemon process.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :return: Start daemon process status (True) | False.
            :rtype: <bool>
            :exceptions: None
        '''
        pid, status = None, False
        verbose_message(Daemon.VERBOSE, verbose, 'start daemon process')
        if self.unix_status:
            with FileProcessId(self.__pid_file_path, 'w+') as pid_file_path:
                pid = pid_file_path.read().strip()
                if bool(pid):
                    error_message(
                        Daemon.VERBOSE, 'file {0} already exist'.format(
                            self.__pid_file_path
                        ), 'daemon already running?'
                    )
                else:
                    self.daemonize(verbose=verbose)
                    self.run()
                    status = True
        return True if status else False

    def stop(self, verbose=False):
        '''
            Stop Daemon process.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :return: Stop daemon process status (True) | False.
            :rtype: <bool>
            :exceptions: None
        '''
        pid, status = None, False
        verbose_message(Daemon.VERBOSE, verbose, 'stop daemon process')
        if self.unix_status:
            with FileProcessId(self.__pid_file_path, 'r') as pid_file_path:
                pid = int(pid_file_path.read().strip())
                if not pid:
                    error_message(Daemon.VERBOSE, 'daemon process running?')
                else:
                    status = self.unix_kill(pid, self.__pid_file_path)
        return True if status else False

    def restart(self, verbose=False):
        '''
            Restart Daemon process.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :return: Restart daemon process status (True) | False.
            :rtype: <bool>
            :exceptions: None
        '''
        status = False
        verbose_message(Daemon.VERBOSE, verbose, 'restart daemon process')
        if self.unix_status:
            status = self.stop(verbose=verbose)
            if status:
                status = self.start(verbose=verbose)
            else:
                error_message(
                    Daemon.VERBOSE, 'faled to restart daemon process'
                )
        else:
            error_message(Daemon.VERBOSE, 'daemon process is active?')
        return True if status else False

    def exit_handler(self, verbose=False):
        '''
            Remove PID file at exit.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: None
        '''
        if self.unix_status:
            if exists(self.__pid_file_path):
                verbose_message(
                    Daemon.VERBOSE, verbose,
                    'removing pid file', self.__pid_file_path
                )
                remove(self.__pid_file_path)
            else:
                error_message(
                    Daemon.VERBOSE, 'check PID file', self.__pid_file_path
                )

    @abstract_method
    def run(self):
        '''
            Run Daemon process.
            Override this method when subclass Daemon.
            It will be called after the process has been
            daemonized by start() or restart().

            :exceptions: None
        '''
        pass

    def __str__(self):
        '''
            Dunder method for Daemon.

            :return: Object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1}, {2})'.format(
            self.__class__.__name__, str(self.__daemon_usage),
            self.__pid_file_path
        )
