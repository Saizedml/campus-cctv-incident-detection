PYTHON ?= python

.PHONY: setup lint test figures dashboard
setup:
	$(PYTHON) -m pip install -e '.[dev,dashboard]'
lint:
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .
test:
	$(PYTHON) -m pytest
figures:
	$(PYTHON) scripts/make_figures.py
dashboard:
	$(PYTHON) -m campus_cctv.dashboard
