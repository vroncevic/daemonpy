# Copyright 2020 Vladimir Roncevic <elektron.ronca@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

FROM debian:10
RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
 tree \
 htop \
 python \
 python-pip \
 python-wheel \
 libyaml-dev

RUN pip install --upgrade setuptools
RUN mkdir /daemonpy/
COPY daemonpy /daemonpy/
COPY setup.py /
COPY requirements.txt /
RUN pip install -r requirements.txt
RUN rm -f requirements.txt
RUN find /daemonpy/ -name "*.editorconfig" -type f -exec rm -Rf {} \;
RUN python setup.py install_lib
RUN python setup.py install_egg_info
RUN rm -rf /daemonpy/
RUN rm -f setup.py
RUN chmod -R 755 /usr/local/lib/python2.7/dist-packages/daemonpy/
RUN tree /usr/local/lib/python2.7/dist-packages/daemonpy/
