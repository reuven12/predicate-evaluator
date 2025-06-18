test:
	docker compose run --rm predicate-tests

lint:
	docker compose run --rm predicate-tests flake8 predicate

format:
	docker compose run --rm predicate-tests black predicate

run:
	docker compose up --build

clean:
	docker compose down --volumes --remove-orphans
