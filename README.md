# Travelbear Server

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


#### Quick start

Docker is required for local development.
Installation instructions are at [docs.docker.com/install](https://docs.docker.com/install/). 

 1. Clone this repo and `cd` into it.
 2. Check everything is working correctly by running the test suite: `make test`.

#### Scripts

Some useful scripts are defined in `Makefile`.

 - `make test` runs the test suite.
To test a specific package specify it with `pkg`.
e.g. `make test pkg=api_public.auth`.
 - `make lint` lints your code for you, be sure to do this before pushing to GitHub as CircleCI
rejects unlinted code.
 - `make ssh` starts a shell on the local server so you can execute arbitrary commands.
This is useful for running Django management commands.
 - `make dev` runs the Django app locally at http://127.0.0.1:8080.
 - `make prod` runs the Django app locally at http://127.0.0.1:80.
