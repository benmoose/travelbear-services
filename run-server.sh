#!/bin/bash

docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run -e stack=development --rm server
