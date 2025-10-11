install:
	python3 -m venv venv
	./venv/bin/pip install paramiko pyyaml

run:
	./venv/bin/python chat.py