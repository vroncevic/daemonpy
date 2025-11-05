#!/bin/bash
#
# @brief   daemonpy
# @version v1.0.1
# @date    Sat Aug 11 09:58:41 2020
# @company None, free software to use 2020
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

rm -rf htmlcov daemonpy_coverage.xml daemonpy_coverage.json .coverage
python3 -m coverage run -m --source=../daemonpy unittest discover -s ./ -p '*_test.py' -vvv
python3 -m coverage html -d htmlcov
python3 -m coverage xml -o daemonpy_coverage.xml 
python3 -m coverage json -o daemonpy_coverage.json
python3 -m coverage report --format=markdown -m
python3 ats_coverage.py -n daemonpy
rm htmlcov/.gitignore
echo "Done"
