install:
	poetry install

build:
	./build.sh

dev:
	poetry run flask --app page_analyzer:app run

test:
	poetry run pytest

lint:
	poetry run flake8 page_analyzer

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

start_psql:
	docker compose up -d

shut_down_psql:
	docker compose down

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml