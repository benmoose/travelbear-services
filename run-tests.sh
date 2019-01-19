#!/bin/bash

docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
    run --rm -e stack=test server pytest \
    --doctest-modules --rootdir travelbear --pyargs "$@"
