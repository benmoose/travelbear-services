#!/bin/bash

export ENVIRONMENT=test

pytest --pyargs "$@"
