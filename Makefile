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
	python init_db.py
