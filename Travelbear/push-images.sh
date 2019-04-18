#!/bin/bash

./operations/build-scrips/push-to-ecr.sh django .
./operations/build-scrips/push-to-ecr.sh nginx operations/nginx
