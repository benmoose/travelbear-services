#!/bin/bash

docker-compose \
    run --rm --no-deps server black --exclude db_layer/migrations ./travelbear $@
