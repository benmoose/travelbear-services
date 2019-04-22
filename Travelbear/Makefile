.PHONY: fmt ssh psql

fmt:
	docker-compose \
		run --entrypoint "sh -c" --rm --no-deps server \
			"black . && isort -rc -q travelbear"

ssh:
	docker-compose \
		run --rm --entrypoint /bin/bash server

psql:
	docker-compose exec -u postgres db psql
