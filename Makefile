.PHONY: setup run lint format type-check

setup:
	pip install -r requirements.txt -r dev-requirements.txt
	docker run --name ps_bot_postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=postgres -e POSTGRES_DB=ps_bot -p 5432:5432 -d postgres:14-alpine
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