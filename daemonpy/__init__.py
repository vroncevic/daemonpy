# -*- coding: UTF-8 -*-

"""
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
     Define class Daemon with attribute(s) and method(s).
     Load a settings and setup operations.
"""

import sys
from os import fork, chdir, setsid, umask, dup2, getpid, remove, kill
from os.path import exists
from atexit import register
from time import sleep
from inspect import stack
from signal import SIGTERM

try:
    from ats_utilities.abstract import abstract_method
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.console_io.error import error_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
except ImportError as error:
    MESSAGE = "\n{0}\n{1}\n".format(__file__, error)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, Free software to use and distributed it.'
__credits__ = ['Vladimir Roncevic']
__license__ = 'GNU General Public License (GPL)'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Daemon(object):
    """
        Define class Daemon with attribute(s) and method(s).
        Load a settings and setup operations.
        It defines:

            :attributes:
                | __slots__ - Setting class slots
                | VERBOSE - Console text indicator for current process-phase
                | __DAEMON_OPERATIONS - Supported Daemon operations
                | __active - Control operations of Daemon process
                | __pid_file - PID file for Daemon process
                | __stdin - Standard input stream file path
                | __stdout - Standard output stream file path
                | __stderr - Standard error stream file path
            :methods:
                | __init__ - Initial constructor
                | daemonize - Create Daemon process
                | delpid - Delete PID file
                | start - Start Daemon process
                | stop - Stop Daemon process
                | restart - Restart Daemon process
                | usage - Checking usage of Daemon process
                | run - Run Daemon process (abstract method)
    """

    __slots__ = (
        'VERBOSE',
        '__DAEMON_OPERATIONS',
        '__active',
        '__pid_file',
        '__stdin',
        '__stdout',
        '__stderr'
    )
    VERBOSE = 'DAEMONPY'
    __DAEMON_OPERATIONS = ['start', 'stop', 'restart']

    def __init__(self, pf, verbose=False):
        """
            Initial constructor.

            :param pf: PID file path
            :type pf: <str>
            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: ATSBadCallError | ATSTypeError
        """
        func = stack()[0][3]
        pf_txt = 'Argument: expected PID file path <str> object'
        pf_msg = "{0} {1} {2}".format('def', func, pf_txt)
        if pf is None or not pf:
            raise ATSBadCallError(pf_msg)
        if not isinstance(pf, str):
            raise ATSTypeError(pf_msg)
        verbose_message(Daemon.VERBOSE, verbose, 'Initial Daemon process')
        self.__stdin = '/dev/null'
        self.__stdout = '/dev/null'
        self.__stderr = '/dev/null'
        self.__pid_file = pf
        self.__active = True

    def daemonize(self, verbose=False):
        """
            Create daemon process.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        verbose_message(Daemon.VERBOSE, verbose, 'Create Daemon process')
        if self.__active:
            try:
                pid = fork()
                if pid > 0:
                    sys.exit(0)
            except OSError as err:
                sys.stderr.write(
                    'fork #1 failed: {0} {1}\n'.format(err.errno, err.strerror)
                )
                sys.exit(1)
            chdir("/")
            setsid()
            umask(0)
            try:
                pid = fork()
                if pid > 0:
                    sys.exit(0)
            except OSError as err:
                sys.stderr.write(
                    'fork #2 failed: {0} {1}\n'.format(err.errno, err.strerror)
                )
                sys.exit(1)
            sys.stdout.flush()
            sys.stderr.flush()
            stdin_file = open(self.__stdin, 'r')
            stdout_file = open(self.__stdout, 'a+')
            stderr_file = open(self.__stderr, 'a+', 0)
            dup2(stdin_file.fileno(), sys.stdin.fileno())
            dup2(stdout_file.fileno(), sys.stdout.fileno())
            dup2(stderr_file.fileno(), sys.stderr.fileno())
            register(self.delpid)
            pid = str(getpid())
            with open(self.__pid_file, 'w+') as pid_file:
                pid_file.write('{0}\n'.format(pid))

    def delpid(self, verbose=False):
        """
            Remove PID file.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        verbose_message(
            Daemon.VERBOSE, verbose, 'Remove PID file', self.__pid_file
        )
        if self.__active:
            remove(self.__pid_file)

    def start(self, verbose=False):
        """
            Start Daemon process.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        pid = None
        verbose_message(Daemon.VERBOSE, verbose, 'Start Daemon process')
        if self.__active:
            try:
                with open(self.__pid_file, 'r') as pid_file:
                    pid = int(pid_file.read().strip())
            except IOError:
                verbose_message(Daemon.VERBOSE, verbose, "{0}".format(
                        'No such file or directory', self.__pid_file
                    )
                )
            if pid:
                sys.stderr.write(
                    'File {0} already exist, Daemon already running?\n'.format(
                        self.__pid_file
                    )
                )
                sys.exit(1)
            self.daemonize()
            self.run()

    def stop(self, verbose=False):
        """
            Stop Daemon process.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        pid = None
        verbose_message(Daemon.VERBOSE, verbose, 'Stop Daemon process')
        if self.__active:
            try:
                with open(self.__pid_file, 'r') as pid_file:
                    pid = int(pid_file.read().strip())
            except IOError as err:
                error_message(Daemon.VERBOSE, "{0}".format(str(err)))
            if not pid:
                sys.stderr.write('Daemon process running?\n')
                return
            try:
                while 1:
                    kill(pid, SIGTERM)
                    sleep(0.1)
            except OSError as err:
                err = str(err)
                if err.find('No such process') > 0:
                    if exists(self.__pid_file):
                        remove(self.__pid_file)
                else:
                    error_message(Daemon.VERBOSE, "{0}".format(err))
                    sys.exit(1)

    def restart(self, verbose=False):
        """
            Restart Daemon process.

            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        verbose_message(Daemon.VERBOSE, verbose, 'Restart Daemon process')
        if self.__active:
            self.stop()
            self.start()

    def usage(self, arguments, verbose=False):
        """
            Checking usage of Daemon process.

            :param arguments: List of arguments
            :type arguments: <list>
            :param verbose: Enable/disable verbose option
            :type verbose: <bool>
            :exceptions: None
        """
        verbose_message(Daemon.VERBOSE, verbose, 'Checking usage')
        if len(arguments) == 2:
            if self.__DAEMON_OPERATIONS[0] == arguments[1]:
                self.start()
            elif self.__DAEMON_OPERATIONS[1] == arguments[1]:
                self.stop()
            elif self.__DAEMON_OPERATIONS[2] == arguments[1]:
                self.restart()
            else:
                error_message(
                    Daemon.VERBOSE, 'usage: {0} start|stop|restart'.format(
                        arguments[0]
                    )
                )
                sys.exit(2)
            sys.exit(0)
        else:
            error_message(
                Daemon.VERBOSE, 'usage: {0} start|stop|restart'.format(
                    arguments[0]
                )
            )
            sys.exit(2)

    @abstract_method
    def run(self):
        """
            Run Daemon process.
            Override this method when subclass Daemon.
            It will be called after the process has been
            daemonized by start() or restart().

            :exceptions: None
        """
        pass
