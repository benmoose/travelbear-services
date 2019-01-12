.PHONY: dev prod test lint ssh

dev:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		up

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml \
		up

test:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm -e stack=test server pytest \
		--doctest-modules --rootdir travelbear --pyargs "$(pkg)"

lint:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm --no-deps server black \
		--exclude db_layer/migrations travelbear

ssh:
	docker-compose -f docker-compose.dev.yml -f docker-compose.yml \
		run --rm server bash
