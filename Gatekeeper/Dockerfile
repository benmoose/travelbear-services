FROM golang:1.12-alpine

WORKDIR /usr/src/app

COPY . .

RUN go build -v -o /tmp/gatekeeper

ENTRYPOINT /tmp/gatekeeper
