#!/bin/bash

set -e

if [[ $1 == "--check" ]]; then
    echo "Checking code..."
    black --check . && isort -rc -q travelbear --check-only
else
    echo "Linting code..."
    black . && isort -rc -q travelbear
fi
