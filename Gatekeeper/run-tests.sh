#!/bin/bash

export ENVIRONMENT=test

export TWILIO_ACCOUNT_SID=test-account-sid
export TWILIO_AUTH_TOKEN=test-auth-token

pytest --pyargs "$@"
