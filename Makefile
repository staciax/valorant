venv=.venv
python=$(venv)/bin/python

default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: report
.SILENT: report
report: # See the coverage report
	$(python) -m coverage report

.PHONY: lint
.SILENT: lint
lint: # Run the linter
	mypy valorant tests
	ruff check valorant tests
	ruff format valorant tests --check

.PHONY: format
.SILENT: format
format: # Format the code
	ruff check valorant tests --fix
	ruff format valorant tests

.PHONY: test
.SILENT: test
test: # Run the tests
	$(python) -m pytest
