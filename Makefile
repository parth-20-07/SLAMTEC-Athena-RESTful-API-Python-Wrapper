# define the name of the virtual environment directory
VENV := .venv

all: venv

$(VENV)/bin/activate: pyproject.toml
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -e .

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 src/robotComms/robotComms.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all venv run clean freeze
