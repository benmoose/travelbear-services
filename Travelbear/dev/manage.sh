#!/bin/bash

set -eu

docker-compose run --rm --entrypoint ./travelbear/manage.py server "$@"
