
install:
	python3 -m venv .
	bin/pip install -r requirements.txt

test:
	bin/pip install -r test-requirements.txt
	bin/pip install -e .
	bin/pytest -sv tests/tests.py
