# define the name of the virtual environment directory
VENV := .venv

all: venv

setup: pyproject.toml
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e .

dev: pyproject.toml
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e .[dev]

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 src/robotComms/robotComms.py

clean:
	rm -rf $(VENV)
	rm -rf .ruff_cache
	rm -rf logs
	find . -type f -name '*.pyc' -delete
	find . -name '__pycache__' -ls -exec rm -rv {} +
	find . -name '*.egg-info' -ls -exec rm -rv {} +

.PHONY: all venv run clean setup dev
