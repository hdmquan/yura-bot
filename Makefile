.PHONY: install lint test build deploy clean run setup

install:
	poetry install

setup: install
	poetry run pre-commit install

lint:
	poetry run black .
	poetry run ruff check .
	poetry run mypy src

test:
	poetry run pytest

build:
	bash scripts/build_lambda.sh

deploy: build
	cd infra && pulumi up

clean:
	rm -rf .build lambda_package.zip
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	poetry run python -m src.handler
