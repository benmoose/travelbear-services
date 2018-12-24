#!/bin/bash

function start_production () {
    gunicorn --pythonpath travelbear \
        django_conf.wsgi -w 4 -b 0.0.0.0:8000 --chdir=/usr/src/app --log-file -
}

start_production
