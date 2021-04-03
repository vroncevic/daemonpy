# -*- coding: UTF-8 -*-

'''
 Module
     unix_operations.py
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
     Defined class UnixOperations with attribute(s) and method(s).
     Created API for operating Unix Like OS processes.
'''

import sys
from os import fork, kill, remove
from os.path import exists
from signal import SIGTERM
from time import sleep

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
except ImportError as error_message:
    MESSAGE = '\n{0}\n{1}\n'.format(__file__, error_message)
    sys.exit(MESSAGE)  # Force close python ATS ##############################

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright 2020, https://vroncevic.github.io/daemonpy'
__credits__ = ['Vladimir Roncevic']
__license__ = 'https://github.com/vroncevic/daemonpy/blob/master/LICENSE'
__version__ = '1.5.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class UnixOperations(object):
    '''
        Defined class UnixOperations with attribute(s) and method(s).
        Created API for operating Unix Like OS processes.
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | __OS_TARGET - List of supported Operating Systems.
                | __NO_PROCESS - No such process message.
                | __unix_status - Unix status (True for Unix Like OS).
            :methods:
                | __init__ - Initial constructor.
                | unix_status - Property methods for set/get operations.
                | first_fork - Make sure that process is not group leader.
                | second_fork - Won't be started merely by opening a terminal.
                | unix_kill - Kill Unix Like OS process.
                | __str__ - Dunder method for object UnixOperations.
    '''

    __slots__ = ('VERBOSE', '__OS_TARGET', '__NO_PROCESS', '__unix_status')
    VERBOSE = 'DAEMONPY::UNIX_OPERATIONS'
    __OS_TARGET = ['linux', 'linux2']
    __NO_PROCESS = 'No such process'

    def __init__(self, verbose=False):
        '''
            Initial constructor.

            :exceptions: None
        '''
        verbose_message(
            UnixOperations.VERBOSE, verbose,
            'init daemon operations'
        )
        self.__unix_status = any([
            sys.platform == target for target in UnixOperations.__OS_TARGET
        ])

    @property
    def unix_status(self):
        '''
            Property method for getting Unix Like OS status.

            :return: Unix Like OS status.
            :rtype: <bool>
            :exceptions: None
        '''
        return self.__unix_status

    @unix_status.setter
    def unix_status(self, unix_status):
        '''
            Property method for setting Unix Like OS status.

            :param unix_status: Unix Like OS status.
            :type unix_status: <bool>
            :exceptions: None
        '''
        self.__unix_status = unix_status

    def first_fork(self, verbose=False):
        '''
            Make sure that process is not group leader.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exit code: 0 (success) | 1 (failed)
            :exceptions: None
        '''
        if self.__unix_status:
            try:
                process_id = fork()
                if process_id > 0:
                    verbose_message(
                        UnixOperations.VERBOSE, verbose, 'first fork'
                    )
                    sys.exit(0)
            except OSError as os_error:
                error_message(
                    'fork #1 failed: {0} {1}\n'.format(
                        os_error.errno, os_error.strerror
                    )
                )
                sys.exit(1)

    def second_fork(self, verbose=False):
        '''
            Won't be started merely by opening a terminal.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exit code: 0 (success) | 1 (failed)
            :exceptions: None
        '''
        if self.__unix_status:
            try:
                process_id = fork()
                if process_id > 0:
                    verbose_message(
                        UnixOperations.VERBOSE, verbose, 'second fork'
                    )
                    sys.exit(0)
            except OSError as os_error:
                error_message(
                    'fork #2 failed: {0} {1}\n'.format(
                        os_error.errno, os_error.strerror
                    )
                )
                sys.exit(1)

    def unix_kill(self, process_id, pid_file_path, verbose=False):
        '''
            Kill Unix Like OS process.

            :param process_id: Process ID.
            :type process_id: <int>
            :param pid_file_path: PID file path.
            :type pid_file_path: <str>
            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status, sleep_time = ATSChecker(), None, False, 0.1
        error, status = checker.check_params([
            ('int:process_id', process_id),
            ('str:pid_file_path', pid_file_path)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        if self.__unix_status:
            try:
                verbose_message(
                    UnixOperations.VERBOSE, verbose,
                    'kill process {0}'.format(process_id)
                )
                while 1:
                    kill(process_id, SIGTERM)
                    sleep(sleep_time)
                    status = True
            except OSError as os_error:
                os_error = str(os_error)
                if os_error.find(UnixOperations.__NO_PROCESS) > 0:
                    if exists(pid_file_path):
                        verbose_message(
                            UnixOperations.VERBOSE, verbose,
                            '{0} with PID: {1}, removing pid file {2}'.format(
                                UnixOperations.__NO_PROCESS,
                                process_id, pid_file_path
                            )
                        )
                        remove(pid_file_path)
                        status = True
                else:
                    error_message(
                        UnixOperations.VERBOSE, '{0}'.format(os_error)
                    )
                    status = False
        return True if status else False

    def __str__(self):
        '''
            Dunder method for UnixOperations.

            :return: Object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1})'.format(
            self.__class__.__name__, str(self.__unix_status)
        )
