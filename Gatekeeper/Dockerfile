FROM golang:1.12-alpine as builder

WORKDIR /usr/src/app

COPY . .

RUN go build -v -o /tmp/gatekeeper

FROM alpine
COPY --from=builder /tmp/gatekeeper /usr/local/bin/gatekeeper

ENTRYPOINT /usr/local/bin/gatekeeper
