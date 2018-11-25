#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run --rm --no-deps server pytest --doctest-modules -W ignore::DeprecationWarning travelbear $@
