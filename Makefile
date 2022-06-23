-include Makefile.options
#####################################################################################
version=0.1
#####################################################################################
test:
	pytest -v
prepare-env:
	python -m venv .venv
install-req:
	pip install -r requirements.txt
run:
	python -m sage.run
#####################################################################################
.PHONY:
	run test prepare-env install-req
