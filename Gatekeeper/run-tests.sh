#!/bin/bash

docker-compose run --rm -e stack=test --entrypoint go gatekeeper \
    test ./...
