#!/bin/bash

docker-compose run --rm --entrypoint ./run-tests.sh server "$@"
