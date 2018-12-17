#!/bin/bash

docker-compose \
    run -e stack=test --rm server pytest --doctest-modules -W ignore::DeprecationWarning \
    --rootdir travelbear --pyargs "$@"
