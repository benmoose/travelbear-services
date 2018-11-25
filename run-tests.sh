#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run -e stack=test --rm --no-deps server pytest --doctest-modules -W ignore::DeprecationWarning travelbear $@
