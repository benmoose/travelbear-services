# TravelBear Server

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


#### Quick start

 - Install Docker
 - Clone the repo
 - Run tests with `./run-tests.sh` (this will take longer on the first run as the images are built)

#### Other commands

`./run-linter.sh` will lint your code for you, be sure to do this before pushing to GitHub as CircleCI
rejects unlinted code.

`./run-command.sh` runs an abritrary command in the server container, useful for running Django management
commands. e.g. `./run-command ./travelbear/manage.py makemigrations`.

`./run-server.sh` runs the Django app locally at http://127.0.0.1:8080.
