# -*- coding: UTF-8 -*-

'''
Module
    daemon_usage.py
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
    Defines class DaemonUsage with attribute(s) and method(s).
    Creates an API for daemon usage.
'''

import sys
from typing import List

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
__version__ = '1.8.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DaemonUsage:
    '''
        Defines class DaemonUsage with attribute(s) and method(s).
        Creates an API for daemon usage.

        It defines:

            :attributes:
                | _PKG_VERBOSE - Console text indicator for process-phase.
                | DAEMON_OPERATIONS - List of supported operations.
                | _usage_status - Daemon usage status.
            :methods:
                | __init__ - Initials DaemonUsage constructor.
                | usage_status - Property methods for set/get operations.
                | check - Checks usage for daemon process.
    '''

    _PKG_VERBOSE: str = 'DAEMONPY::DAEMON_USAGE'
    DAEMON_OPERATIONS: List[str] = ['start', 'stop', 'restart']

    def __init__(self, verbose: bool = False) -> None:
        '''
            Initials DaemonUsage constructor.

            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: None
        '''
        verbose_message(verbose, [f'{self._PKG_VERBOSE} init usage'])
        self._usage_status: int = 0

    @property
    def usage_status(self) -> int:
        '''
            Property method for getting daemon usage status.

            :return: Daemon usage status
            :rtype: <int>
            :exceptions: None
        '''
        return self._usage_status

    @usage_status.setter
    def usage_status(self, usage_status: int) -> None:
        '''
            Property method for setting daemon usage status.

            :param usage_status: Daemon usage status
            :type usage_status: <int>
            :exceptions: None
        '''
        self._usage_status = usage_status

    def check(self, daemon_operation: str, verbose: bool = False):
        '''
            Checks usage of Daemon process.

            :param daemon_operation: Daemon operation
            :type daemon_operation: <str>
            :param verbose: Enable/Disable verbose option
            :type verbose: <bool>
            :exceptions: ATSTypeError | ATSValueError
        '''
        error_msg: str | None = None
        error_id: int | None = None
        checker: ATSChecker = ATSChecker()
        error_msg, error_id = checker.check_params([
            ('str:daemon_operation', daemon_operation)
        ])
        if error_id == checker.TYPE_ERROR:
            raise ATSTypeError(error_msg)
        if not bool(daemon_operation):
            raise ATSValueError('missing daemon operation')
        verbose_message(verbose, [f'{self._PKG_VERBOSE} checking usage'])
        for index, option in enumerate(self.DAEMON_OPERATIONS):
            if option == daemon_operation:
                self._usage_status = index
        if daemon_operation not in self.DAEMON_OPERATIONS:
            self._usage_status = 127
            error_message([
                f'{self._PKG_VERBOSE} usage: {0}',
                '|'.join(self.DAEMON_OPERATIONS)
            ])
        verbose_message(
            verbose,
            [f'{self._PKG_VERBOSE} usage status', self._usage_status]
        )
