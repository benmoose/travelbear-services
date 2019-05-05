#!/bin/bash

[[ -z ${CIRCLE_BRANCH} ]] && exit 1
[[ -z ${AWS_ECR_ACCOUNT_URL} ]] && exit 1

build-scrips/push-to-ecr.sh django operations/django/Dockerfile
build-scrips/push-to-ecr.sh nginx operations/nginx/Dockerfile
