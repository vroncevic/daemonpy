# -*- coding: UTF-8 -*-

'''
 Module
     daemon_usage.py
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
     Defined class DaemonUsage with attribute(s) and method(s).
     Created API for daemon usage.
'''

import sys

try:
    from ats_utilities.checker import ATSChecker
    from ats_utilities.console_io.error import error_message
    from ats_utilities.console_io.verbose import verbose_message
    from ats_utilities.exceptions.ats_type_error import ATSTypeError
    from ats_utilities.exceptions.ats_bad_call_error import ATSBadCallError
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


class DaemonUsage(object):
    '''
        Defined class DaemonUsage with attribute(s) and method(s).
        Created API for daemon usage.
        It defines:

            :attributes:
                | __slots__ - Setting class slots.
                | VERBOSE - Console text indicator for current process-phase.
                | DAEMON_OPERATIONS - list of supported operations.
                | __usage_status - Daemon usage status.
            :methods:
                | __init__ - Initial constructor.
                | usage_status - Property methods for set/get operations.
                | check - Checking usage of Daemon process.
                | __str__ - Dunder method for object DaemonUsage.
    '''

    __slots__ = ('VERBOSE', 'DAEMON_OPERATIONS', '__usage_status')
    VERBOSE = 'DAEMONPY::DAEMON_USAGE'
    DAEMON_OPERATIONS = ['start', 'stop', 'restart']

    def __init__(self, verbose=False):
        '''
            Initial constructor.

            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(DaemonUsage.VERBOSE, verbose, 'init usage')
        self.__usage_status = 0

    @property
    def usage_status(self):
        '''
            Property method for getting daemon usage status.

            :return: Daemon usage status.
            :rtype: <int>
            :exceptions: None
        '''
        return self.__usage_status

    @usage_status.setter
    def usage_status(self, usage_status):
        '''
            Property method for setting daemon usage status.

            :param usage_status: Daemon usage status.
            :type usage_status: <int>
            :exceptions: None
        '''
        self.__usage_status = usage_status

    def check(self, daemon_operation, verbose=False):
        '''
            Checking usage of Daemon process.

            :param daemon_operation: Daemon operation.
            :type daemon_operation: <str>
            :param verbose: Enable/disable verbose option.
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSBadCallError
        '''
        checker, error, status = ATSChecker(), None, False
        error, status = checker.check_params([
            ('str:daemon_operation', daemon_operation)
        ])
        if status == ATSChecker.TYPE_ERROR:
            raise ATSTypeError(error)
        if status == ATSChecker.VALUE_ERROR:
            raise ATSBadCallError(error)
        verbose_message(DaemonUsage.VERBOSE, verbose, 'checking usage')
        for index, option in enumerate(DaemonUsage.DAEMON_OPERATIONS):
            if option == daemon_operation:
                self.__usage_status = index
        if daemon_operation not in DaemonUsage.DAEMON_OPERATIONS:
            self.__usage_status = 127
            error_message(
                DaemonUsage.VERBOSE, 'usage: {0}'.format(
                    '|'.join(DaemonUsage.DAEMON_OPERATIONS)
                )
            )
        verbose_message(
            DaemonUsage.VERBOSE, verbose, 'usage status', self.__usage_status
        )

    def __str__(self):
        '''
            Dunder method for DaemonUsage.

            :return: Object in a human-readable format.
            :rtype: <str>
            :exceptions: None
        '''
        return '{0} ({1})'.format(
            self.__class__.__name__, str(self.__usage_status)
        )
