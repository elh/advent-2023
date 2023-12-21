all:
	@python all.py --skip=$(SKIP)

.PHONY: lint
lint:
	@mypy --ignore-missing-imports .
	@ruff check .

# TODO: update to add `--line-length 120` later
.PHONY: pretty
pretty:
	@black .

.PHONY: good
good: lint pretty
