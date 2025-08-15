# Minimal Makefile for running the demo with a local venv + SQLite
# Usage:
#   make demo     # (default) create venv, install, run demo_check.py
#   make clean    # remove venv and caches

SHELL     := /bin/bash
.DEFAULT_GOAL := demo

VENV      ?= venv
PYTHON    ?= python3
PIP       := $(VENV)/bin/pip
PY        := $(VENV)/bin/python

.PHONY: venv install demo local clean

venv:
	@test -d "$(VENV)" || $(PYTHON) -m venv "$(VENV)"
	@$(PIP) install --upgrade pip setuptools wheel

install: venv
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		echo "requirements.txt not found; skipping pip install"; \
	fi

demo: install
	@echo "Running demo_check.py with local SQLite (DATABASE_URL unset -> auto file) ..."
	@"$(PY)" demo_check.py

# alias for your old target name
local: demo

clean:
	rm -rf "$(VENV)" __pycache__ */__pycache__ .pytest_cache
