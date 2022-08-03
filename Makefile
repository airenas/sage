-include Makefile.options
#####################################################################################
version=0.1
#####################################################################################
prepare-env:
	python -m venv .venv
install/req:
	pip install -r requirements.txt
install/test-req:
	pip install -r requirements_test.txt

install/deps:
	sudo apt install -y portaudio19-dev python3-pyaudio
run:
	python -m sage.run

test:
	pytest -v --log-level=INFO
#####################################################################################
.PHONY:
	run test prepare-env install-req
