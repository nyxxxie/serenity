.PHONY: test
test:
	pytest -v

.PHONY: venv
venv:
	. ./venv/bin/activate
