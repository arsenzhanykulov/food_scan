.PHONY: format lint

format:
	black .
	isort .

lint:
	flake8 .
	isort . --check-only

lint-fix:
	isort .