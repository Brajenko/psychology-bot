.PHONY: setup run lint format type-check

setup:
	pip install -r requirements.txt -r dev-requirements.txt
	docker compose up -d pg_database
	alembic upgrade head

run:
	python -m bot

docker:
	docker compose up -d
	docker-compose exec bot alembic upgrade head

lint:
	ruff check .

format:
	ruff check . --fix

type-check:
	mypy --check-untyped-defs .

rev:
	@echo "Enter rev msg: "; \
	read msg; \
	alembic revision --autogenerate -m "$$msg"

migrate:
	alembic upgrade head

init_db:
	docker compose cp ./init_polls.sql pg_database:/init_polls.sql
	docker compose exec pg_database psql ps_bot -U postgres -f /init_polls.sql