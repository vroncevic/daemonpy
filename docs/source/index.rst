Creating Daemon process
-----------------------

**daemonpy** is package for creating Daemon processes.

Developed in `python <https://www.python.org/>`_ code: **100%**.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

|Python package| |GitHub issues| |Documentation Status| |GitHub contributors|

.. |Python package| image:: https://github.com/vroncevic/daemonpy/workflows/Python%20package%20daemonpy/badge.svg
   :target: https://github.com/vroncevic/daemonpy/workflows/Python%20package/badge.svg?branch=master

.. |GitHub issues| image:: https://img.shields.io/github/issues/vroncevic/daemonpy.svg
   :target: https://github.com/vroncevic/daemonpy/issues

.. |GitHub contributors| image:: https://img.shields.io/github/contributors/vroncevic/daemonpy.svg
   :target: https://github.com/vroncevic/daemonpy/graphs/contributors

.. |Documentation Status| image:: https://readthedocs.org/projects/daemonpy/badge/?version=latest
   :target: https://daemonpy.readthedocs.io/projects/daemonpy/en/latest/?badge=latest

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   self
   modules

Installation
-------------

|Install Python2 Package| |Install Python3 Package|

.. |Install Python2 Package| image:: https://github.com/vroncevic/daemonpy/workflows/Install%20Python2%20Package%20daemonpy/badge.svg
   :target: https://github.com/vroncevic/daemonpy/workflows/Install%20Python2%20Package%20daemonpy/badge.svg?branch=master

.. |Install Python3 Package| image:: https://github.com/vroncevic/daemonpy/workflows/Install%20Python3%20Package%20daemonpy/badge.svg
   :target: https://github.com/vroncevic/daemonpy/workflows/Install%20Python3%20Package%20daemonpy/badge.svg?branch=master

Navigate to release `page`_ download and extract release archive.

.. _page: https://github.com/vroncevic/daemonpy/releases

To install this set of modules type the following:

.. code-block:: bash

    tar xvzf daemonpy-x.y.z.tar.gz
    cd daemonpy-x.y.z
    # python2
    pip install -r requirements.txt
    python setup.py install_lib
    python setup.py install_egg_info
    # python3
    pip3 install -r requirements.txt
    python3 setup.py install_lib
    python3 setup.py install_egg_info

You can use Docker to create image/container, or You can use pip to install:

.. code-block:: bash

    # python2
    pip install daemonpy
    # python3
    pip3 install daemonpy

|GitHub docker checker|

.. |GitHub docker checker| image:: https://github.com/vroncevic/daemonpy/workflows/daemonpy%20docker%20checker/badge.svg
   :target: https://github.com/vroncevic/daemonpy/actions?query=workflow%3A%22daemonpy+docker+checker%22

Usage
-----

Create short example:

.. code-block:: python

    #!/usr/bin/env python

    '''
     Module
         mydaemon.py
     Copyright
         Copyright (C) 2020 Vladimir Roncevic <elektron.ronca@gmail.com>
         mydaemon is free software: you can redistribute it and/or modify it
         under the terms of the GNU General Public License as published by the
         Free Software Foundation, either version 3 of the License, or
         (at your option) any later version.
         mydaemon is distributed in the hope that it will be useful, but
         WITHOUT ANY WARRANTY; without even the implied warranty of
         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
         See the GNU General Public License for more details.
         You should have received a copy of the GNU General Public License along
         with this program. If not, see <http://www.gnu.org/licenses/>.
     Info
         Define class MyDaemon with attribute(s) and method(s).
         Set an operation for Daemon process.
    '''

    from sys import exit, argv
    from time import sleep

    try:
        from daemonpy import Daemon
    except ImportError as ats_error:
        MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error)
        exit(MESSAGE)  # Force close python ATS ##############################


    class MyDaemon(Daemon):
        '''
            Define class MyDaemon with attribute(s) and method(s).
            Set an operation for Daemon process.
            It defines:

                :attributes:
                    | None
                :methods:
                    | run - Run Daemon process (defined method)
        '''
        def run(self):
            '''
                Run Daemon process with time sleep example.

                :exceptions: None
            '''
            while True:
                sleep(1)

    if __name__ == '__main__':
        DAEMON = MyDaemon('/tmp/daemon-example.pid')
        DAEMON.usage(sys.argv[1])

Dependencies
-------------

**daemonpy** requires next modules and libraries:

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

Library structure
------------------

**daemonpy** is based on OOP:

Code structure:

.. code-block:: bash

    daemonpy/
    ├── daemon_usage.py
    ├── file_descriptor.py
    ├── file_process_id.py
    ├── __init__.py
    └── unix_operations.py

Copyright and licence
----------------------

|License: GPL v3| |License: Apache 2.0|

.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |License: Apache 2.0| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0

Copyright (C) 2020 by `vroncevic.github.io/daemonpy <https://vroncevic.github.io/daemonpy>`_

**daemonpy** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 2.x/3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

|Python Software Foundation|

.. |Python Software Foundation| image:: https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|Donate|

.. |Donate| image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif
   :target: https://psfmember.org/index.php?q=civicrm/contribute/transact&reset=1&id=2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
