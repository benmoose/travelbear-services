#!/bin/bash

command_prefix=""

if [ "$1" != "/bin/bash" ]; then
    command_prefix="travelbear/manage.py"
fi


docker-compose -f docker-compose.yml -f docker-compose.dev.yml \
    run server $command_prefix $@
