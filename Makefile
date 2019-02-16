.PHONY: dev prod build-dev build-prod lint ssh psql

dev:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		up --remove-orphans

prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.yml \
		up --remove-orphans

build-dev:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		build

build-prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.yml \
		build

fmt:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm --no-deps server sh -c "black . && isort -rc -q travelbear"

ssh:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm server bash

psql:
	docker-compose exec -u postgres db psql
