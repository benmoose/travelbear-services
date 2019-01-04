.PHONY: dev prod test lint ssh

dev:
	docker-compose up

prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up

test:
	docker-compose run --rm \
		-e stack=test server pytest --doctest-modules \
		--rootdir travelbear --pyargs "$(pkg)"

lint:
	docker-compose run --rm \
		--no-deps server black --exclude db_layer/migrations \
		travelbear

ssh:
	docker-compose run --rm \
		server bash
