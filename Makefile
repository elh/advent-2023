.PHONY: lint
lint:
	@ruff check .

.PHONY: pretty
pretty:
	@black .
