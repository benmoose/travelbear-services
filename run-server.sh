#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=travelbear.django_conf.settings

docker-compose -f docker-compose.yml -f docker-compose.dev.yml run server
