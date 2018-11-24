#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run --rm --no-deps server black --exclude db_layer/migrations ./travelbear $@
