Creating Daemon process
-----------------------

☯️ **daemonpy** is package for creating Daemon processes.

Developed in 🐍 `python <https://www.python.org/>`_ code.

|codecov| |circleci|

.. |codecov| image:: https://codecov.io/gh/vroncevic/daemonpy/branch/dev/graph/badge.svg
   :target: https://codecov.io/gh/vroncevic/daemonpy

.. |circleci| image:: https://circleci.com/gh/vroncevic/daemonpy/tree/master.svg
   :target: https://circleci.com/gh/vroncevic/daemonpy/tree/master

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

|python checker| |python package| |github issues| |documentation status| |github contributors|

.. |python checker| image:: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python_checker?style=flat&label=daemonpy%20python%20checker
   :target: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python_checker

.. |python package| image:: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_package_checker?style=flat&label=daemonpy%20package%20checker
   :target: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_package_checker

.. |github issues| image:: https://img.shields.io/github/issues/vroncevic/daemonpy.svg
   :target: https://github.com/vroncevic/daemonpy/issues

.. |github contributors| image:: https://img.shields.io/github/contributors/vroncevic/daemonpy.svg
   :target: https://github.com/vroncevic/daemonpy/graphs/contributors

.. |documentation status| image:: https://readthedocs.org/projects/daemonpy/badge/?version=master
   :target: https://daemonpy.readthedocs.io/projects/daemonpy/en/master/?badge=master

.. toctree::
   :maxdepth: 4
   :caption: contents

   self
   modules

Installation
-------------

|install python2 package| |install python3 package|

.. |install python2 package| image:: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python2_build?style=flat&label=daemonpy%20python2%20build
   :target: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python2_build

.. |install python3 package| image:: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python3_build?style=flat&label=daemonpy%20python3%20build
   :target: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python3_build

|ubuntu linux os|

.. |ubuntu linux os| image:: https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/ubuntuxis.png

Navigate to release `page`_ download and extract release archive 📦.

.. _page: https://github.com/vroncevic/daemonpy/releases

To install **daemonpy** 📦 run

.. code-block:: bash

    tar xvzf daemonpy-x.y.z.tar.gz
    cd daemonpy-x.y.z
    # python2
    pip install -r requirements.txt
    python -m build
    pip install dist/daemonpy-x.y.z-py2-none-any.whl
    # python3
    pip3 install -r requirements.txt
    python3 -m build
    pip3 install dist/daemonpy-x.y.z-py3-none-any.whl

Or type the following

.. code-block:: bash

    tar xvzf daemonpy-x.y.z.tar.gz
    cd daemonpy-x.y.z/
    # python2
    pip install -r requirements.txt
    python setup.py install_lib
    python setup.py install_egg_info
    # pyton3
    pip3 install -r requirements.txt
    python3 setup.py install_lib
    python3 setup.py install_egg_info

You can use Docker to create image/container, or You can use pip to install 📦

.. code-block:: bash

    # python2
    pip install daemonpy
    # python3
    pip3 install daemonpy

|github docker checker|

.. |github docker checker| image:: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_docker_checker?style=flat&label=daemonpy%20docker%20checker
   :target: https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_docker_checker

Usage
-----

Create short example

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
         Defined class MyDaemon with attribute(s) and method(s).
         Set an operation for Daemon process.
    '''

    import sys
    from time import sleep

    try:
        from daemonpy import Daemon
    except ImportError as ats_error:
        MESSAGE = '\n{0}\n{1}\n'.format(__file__, ats_error)
        sys.exit(MESSAGE)  # Force close python ATS ##############################


    class MyDaemon(Daemon):
        '''
            Defined class MyDaemon with attribute(s) and method(s).
            Set an operation for Daemon process.
            It defines:

                :attributes:
                    | None
                :methods:
                    | run - run Daemon process (defined method).
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

**daemonpy** requires next modules and libraries

* `ats-utilities - Python App/Tool/Script Utilities <https://pypi.org/project/ats-utilities/>`_

Package structure
------------------

**daemonpy** is based on OOP.

🧰 Package structure

.. code-block:: bash

    daemonpy/
    ├── daemon_usage.py
    ├── file_descriptor.py
    ├── file_process_id.py
    ├── __init__.py
    └── unix_operations.py

Copyright and licence
----------------------

|license: gpl v3| |license: apache 2.0|

.. |license: gpl v3| image:: https://img.shields.io/badge/license-gplv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0

.. |license: apache 2.0| image:: https://img.shields.io/badge/license-apache%202.0-blue.svg
   :target: https://opensource.org/licenses/apache-2.0

Copyright (C) 2020 by `vroncevic.github.io/daemonpy <https://vroncevic.github.io/daemonpy>`_

**daemonpy** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 2.x/3.x or,
at your option, any later version of Python 3 you may have available.

🌎 🌍 🌏 Lets help and support PSF.

|python software foundation|

.. |python software foundation| image:: https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/psf-logo-alpha.png
   :target: https://www.python.org/psf/

|donate|

.. |donate| image:: https://www.paypalobjects.com/en_us/i/btn/btn_donatecc_lg.gif
   :target: https://psfmember.org/index.php?q=civicrm/contribute/transact&reset=1&id=2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
