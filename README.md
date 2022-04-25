<img align="right" src="https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/daemonpy_logo.png" width="25%">

# Creating Daemon process

☯️ **daemonpy** is package for creating Daemon processes.

Developed in 🐍 **[python](https://www.python.org/)** code.

[![codecov](https://codecov.io/gh/vroncevic/daemonpy/branch/dev/graph/badge.svg?token=NKYH7UGEYS)](https://codecov.io/gh/vroncevic/daemonpy)
[![circleci](https://circleci.com/gh/vroncevic/daemonpy/tree/master.svg?style=svg)](https://circleci.com/gh/vroncevic/daemonpy/tree/master)

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

[![daemonpy python checker](https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python_checker?style=flat&label=daemonpy%20python%20checker)](https://github.com/vroncevic/daemonpy/actions/workflows/daemonpy_python_checker.yml) [![daemonpy package checker](https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_package_checker?style=flat&label=daemonpy%20package%20checker)](https://github.com/vroncevic/daemonpy/actions/workflows/daemonpy_package_checker.yml) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/daemonpy.svg)](https://github.com/vroncevic/daemonpy/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/daemonpy.svg)](https://github.com/vroncevic/daemonpy/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
    - [Install using pip](#install-using-pip)
    - [Install using build](#install-using-build)
    - [Install using py setup](#install-using-py-setup)
    - [Install using docker](#install-using-docker)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Package structure](#package-structure)
- [Docs](#docs)
- [Contributing](#contributing)
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

Used next development environment

![debian linux os](https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/ubuntuxis.png)

[![daemonpy python2 build](https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python2_build?style=flat&label=daemonpy%20python2%20build)](https://github.com/vroncevic/daemonpy/actions/workflows/daemonpy_python2_build.yml) [![daemonpy python3 build](https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_python3_build?style=flat&label=daemonpy%20python3%20build)](https://github.com/vroncevic/daemonpy/actions/workflows/daemonpy_python3_build.yml)

Currently there are three ways to install package

- Install process based on using pip
- Install process based on build (setuptools)
- Install process based on setup.py (setuptools)
- Install process based on docker mechanism

##### Install using pip

Python 📦 is located at **[pypi.org](https://pypi.org/project/daemonpy/)**.

You can install by using pip

```bash
# python2
pip install daemonpy
# python3
pip3 install daemonpy
```

##### Install using build

Navigate to **[release page](https://github.com/vroncevic/daemonpy/releases)** download and extract release archive 📦.

To install **daemonpy**, run

```bash
tar xvzf daemonpy-x.y.z.tar.gz
cd daemonpy-x.y.z
# python2
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python2 get-pip.py
python2 -m pip install --upgrade setuptools
python2 -m pip install --upgrade pip
python2 -m pip install --upgrade build
pip install -r requirements.txt
python -m build --no-isolation --wheel
pip install dist/daemonpy-x.y.z-py2-none-any.whl
# python3
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py 
python3 -m pip install --upgrade setuptools
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
pip3 install -r requirements.txt
python3 -m build --no-isolation --wheel
pip3 install dist/daemonpy-x.y.z-py3-none-any.whl
```

##### Install using py setup

Navigate to **[release page](https://github.com/vroncevic/daemonpy/releases)** download and extract release archive 📦.

To install **daemonpy** locate and run setup.py with arguments

```bash
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
```

##### Install using docker

You can use Dockerfile to create image/container 🚢.

[![daemonpy docker checker](https://img.shields.io/github/workflow/status/vroncevic/daemonpy/daemonpy_docker_checker?style=flat&label=daemonpy%20docker%20checker)](https://github.com/vroncevic/daemonpy/actions/workflows/daemonpy_docker_checker.yml)

### Usage

Create short example

```python
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
```

### Dependencies

These modules requires other modules and libraries (Python 2.x/3.x)

- [daemonpy - Python App/Tool/Script Utilities](https://pypi.org/project/daemonpy/)

### Package structure

**daemonpy** is based on OOP.

🧰 Package structure

```bash
daemonpy/
├── daemon_usage.py
├── file_descriptor.py
├── file_process_id.py
├── __init__.py
└── unix_operations.py
```

### Docs

[![documentation status](https://readthedocs.org/projects/ats-utilities/badge/?version=master)](https://ats-utilities.readthedocs.io/projects/ats-utilities/en/master/?badge=master)

📗 More documentation and info at

- [daemonpy.readthedocs.io](https://daemonpy.readthedocs.io/en/latest/)
- [www.python.org](https://www.python.org/)

### Contributing

🌎 🌍 🌏 [Contributing to daemonpy](CONTRIBUTING.md)

### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2020 by [vroncevic.github.io/daemonpy](https://vroncevic.github.io/daemonpy/)

**daemonpy** is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 2.x/3.x or,
at your option, any later version of Python 3 you may have available.

Lets help and support PSF.

[![Python Software Foundation](https://raw.githubusercontent.com/vroncevic/daemonpy/dev/docs/psf-logo-alpha.png)](https://www.python.org/psf/)

[![Donate](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://psfmember.org/index.php?q=civicrm/contribute/transact&reset=1&id=2)
