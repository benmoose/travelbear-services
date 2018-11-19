#!/usr/bin/env bash -x

docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run -e DJANGO_SETTINGS_MODULE=django_conf.settings \
    server pytest --doctest-modules travelbear $@
