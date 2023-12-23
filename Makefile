all:
	@python all.py --skip=$(SKIP)

.PHONY: lint
lint:
	@mypy --ignore-missing-imports .
	@ruff check .

.PHONY: pretty
pretty:
	@black .

.PHONY: good
good: lint pretty
