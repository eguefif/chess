.PHONY: test install

bin/pip:
	python3 -m venv .

install: bin/pip
	bin/pip install -r requirements.txt

clean:
	rm -rf bin lib include

bin/pytest: bin/pip
	bin/pip install -r test-requirements.txt
	bin/pip install -e .

test:	install bin/pytest
	bin/pytest tests/tests.py
