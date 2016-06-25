#!/bin/bash
WORKING_DIR=/Users/robot/django-scrapy
ACTIVATE_PATH=~/.virtualenvs/django-scrapy/activate
cd ${WORKING_DIR}
source ${ACTIVATE_PATH}
exec $@