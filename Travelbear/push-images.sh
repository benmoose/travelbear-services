#!/bin/bash

./operations/build-scrips/push-to-ecr.sh django operations/django/Dockerfile
./operations/build-scrips/push-to-ecr.sh nginx operations/nginx/Dockerfile
