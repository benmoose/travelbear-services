.PHONY: dev prod test lint ssh

dev:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		up

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml \
		up

lint:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm --no-deps server black \
		--exclude db_layer/migrations travelbear --exclude django_conf/settings.py

ssh:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm server bash
