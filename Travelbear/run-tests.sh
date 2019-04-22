#!/bin/bash

docker-compose run --rm -e ENVIRONMENT=test --entrypoint pytest server "$@"
