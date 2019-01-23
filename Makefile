.PHONY: dev prod build lint ssh psql

dev:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		up --remove-orphans

prod:
	docker-compose -f docker-compose.prod.yml -f docker-compose.yml \
		up --remove-orphans

build:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		build

lint:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm --no-deps server black \
		--exclude db_layer/migrations travelbear --exclude django_conf/settings.py

ssh:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm server bash

psql:
	docker-compose exec -u postgres db psql
