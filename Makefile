.PHONY: lint
lint:
	black src/ --check
	flake8 src/
	mypy src/
	isort src/ --check-only

