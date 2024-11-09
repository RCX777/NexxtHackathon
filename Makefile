VIRTUALENV=.venv

.PHONY: venv freeze clean

all: venv

venv:
	test -d $(VIRTUALENV) || python3 -m venv $(VIRTUALENV)
	. $(VIRTUALENV)/bin/activate; pip install -Ur requirements.txt

freeze:
	pip freeze > requirements.txt

run:
	flask run

clean:
	rm -rf $(VIRTUALENV)
	find -iname "*.pyc" -delete

