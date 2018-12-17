#!/bin/bash

docker-compose \
    run --rm server python travelbear/manage.py runserver 0.0.0.0:8000
