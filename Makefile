# define the name of the virtual environment directory
VENV := .venv

all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

venv: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 src/robotComms/robotComms.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

freeze:
	./$(VENV)/bin/pip >> requirements.txt

.PHONY: all venv run clean freeze
