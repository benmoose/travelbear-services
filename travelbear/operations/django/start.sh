#!/bin/bash

function start_production () {
    gunicorn --pythonpath /usr/src/app/travelbear \
        django_conf.wsgi -w 2 -b 0.0.0.0:8000
}

start_production
