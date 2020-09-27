# Creating Daemon process

**daemonpy** is package creating Daemon processes.

Developed in [python](https://www.python.org/) code: **100%**.

The README is used to introduce the modules and provide instructions on
how to install the modules, any machine dependencies it may have and any
other information that should be provided before the modules are installed.

![Python package](https://github.com/vroncevic/daemonpy/workflows/Python%20package%20daemonpy/badge.svg?branch=master) [![GitHub issues open](https://img.shields.io/github/issues/vroncevic/daemonpy.svg)](https://github.com/vroncevic/daemonpy/issues) [![GitHub contributors](https://img.shields.io/github/contributors/vroncevic/daemonpy.svg)](https://github.com/vroncevic/daemonpy/graphs/contributors)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Library structure](#library-structure)
- [Docs](#docs)
- [Copyright and Licence](#copyright-and-licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

### Installation

![Install Python2 Package](https://github.com/vroncevic/daemonpy/workflows/Install%20Python2%20Package%20daemonpy/badge.svg?branch=master) ![Install Python3 Package](https://github.com/vroncevic/daemonpy/workflows/Install%20Python3%20Package%20daemonpy/badge.svg?branch=master)

Navigate to **[release page](https://github.com/vroncevic/daemonpy/releases)** download and extract release archive.

To install modules, locate and run setup.py, type the following:
```
tar xvzf daemonpy-x.y.z.tar.gz
cd daemonpy-x.y.z
pip install -r requirements.txt
```

Install lib process
```
python setup.py install_lib
running install_lib
running build_py
creating build
creating build/lib.linux-x86_64-2.7
creating build/lib.linux-x86_64-2.7/daemonpy
copying daemonpy/__init__.py -> build/lib.linux-x86_64-2.7/daemonpy
creating /usr/local/lib/python2.7/dist-packages/daemonpy
copying build/lib.linux-x86_64-2.7/daemonpy/__init__.py -> /usr/local/lib/python2.7/dist-packages/daemonpy
byte-compiling /usr/local/lib/python2.7/dist-packages/daemonpy/__init__.py to __init__.pyc
```

Install lib egg info
```
python setup.py install_egg_info
running install_egg_info
running egg_info
creating daemonpy.egg-info
writing requirements to daemonpy.egg-info/requires.txt
writing daemonpy.egg-info/PKG-INFO
writing top-level names to daemonpy.egg-info/top_level.txt
writing dependency_links to daemonpy.egg-info/dependency_links.txt
writing manifest file 'daemonpy.egg-info/SOURCES.txt'
reading manifest file 'daemonpy.egg-info/SOURCES.txt'
writing manifest file 'daemonpy.egg-info/SOURCES.txt'
Copying daemonpy.egg-info to /usr/local/lib/python2.7/dist-packages/daemonpy-1.0.0.egg-info
```

Or You can use docker to create image/container.

### Usage

Create short example:
```python
#!/usr/bin/env python

"""
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
"""

import sys
from time import sleep

try:
    from daemonpy import Daemon
except ImportError as error:
    MESSAGE = "\n{0}\n{1}\n".format(__file__, error)
    sys.exit(MESSAGE)  # Force close python ATS ##############################


class MyDaemon(Daemon):
    """
        Define class MyDaemon with attribute(s) and method(s).
        Set an operation for Daemon process.
        It defines:

            :attributes:
                | None
            :methods:
                | run - Run Daemon process (defined method)
    """
    def run(self):
        """
            Run Daemon process with time sleep example.

            :exceptions: None
        """
        while True:
            sleep(1)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-example.pid')
    daemon.usage(sys.argv)
```

### Dependencies

These modules requires other modules and libraries (Python 2.x/3.x):
* [ats-utilities - Python App/Tool/Script Utilities](https://pypi.org/project/ats-utilities/)

### Library structure

**daemonpy** is based on OOP:

Library structure:
```
.
├── daemonpy/
│   └── __init__.py
└── setup.py
```

### Docs

[![Documentation Status](https://readthedocs.org/projects/daemonpy/badge/?version=latest)](https://daemonpy.readthedocs.io/projects/daemonpy/en/latest/?badge=latest)

More documentation and info at:
* [daemonpy.readthedocs.io](https://daemonpy.readthedocs.io/en/latest/)
* [www.python.org](https://www.python.org/)

### Copyright and Licence

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Copyright (C) 2020 by [vroncevic.github.io/daemonpy](https://vroncevic.github.io/daemonpy/)

This tool is free software; you can redistribute it and/or modify
it under the same terms as Python itself, either Python version 2.x/3.x or,
at your option, any later version of Python 3 you may have available.
