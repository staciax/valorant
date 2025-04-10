default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: report
.SILENT: report
report: # See the coverage report
	uv run coverage report

.PHONY: lint
.SILENT: lint
lint: # Run the linter
	uv run mypy valorant tests
	uv run ruff check valorant tests
	uv run ruff format valorant tests --check

.PHONY: format
.SILENT: format
format: # Format the code
	uv run ruff check valorant tests --fix
	uv run ruff format valorant tests

.PHONY: test
.SILENT: test
test: # Run the tests
	uv run pytest
