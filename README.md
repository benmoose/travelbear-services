# Travelbear Server

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


#### Quick start

Docker is required for local development.
Installation instructions are at [docs.docker.com/install](https://docs.docker.com/install/). 

 1. Clone this repo and `cd` into it.
 2. Check everything is working correctly by running the test suite: `./run-tests.sh`.
 3. Run the server locally with `make dev`

#### Scripts

The test suite can be run with `./run-tests.sh`.
```py
# to run a specific package or module
./run-tests.sh api_public.auth
# to run a specific test
./run-tests.sh api_public.auth.auth_decorators_test::test_require_jwt_auth_authenticated
```

Other useful scripts are defined in `Makefile`.

 - `make fmt` formats your code for you (following the [Black code style](https://black.readthedocs.io/en/stable/the_black_code_style.html)).
    Be sure to do this before pushing to GitHub as CircleCI rejects unformatted code.
 - `make ssh` starts a shell on the local server so you can execute arbitrary commands.
This is useful for running Django management commands.
 - `make dev` runs the Django app locally at http://127.0.0.1:8080.
 - `make prod` runs the Django app locally at http://127.0.0.1:80.
