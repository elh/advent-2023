all:
	@python all.py

.PHONY: lint
lint:
	@mypy .
	@ruff check .

.PHONY: pretty
pretty:
	@black .
