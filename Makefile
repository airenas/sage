-include Makefile.options
latex-url?=https://sinteze-test.intelektika.lt/latex-renderer/renderLatex
a2f-url?=localhost:50051
a2f-name?=/World/audio2face/PlayerStreaming
kaldi-url?=ws://localhost:9090/client/ws/speech
greetOnConnect?=--no-greet_on_connect
#####################################################################################
version=0.1
#####################################################################################
prepare-env:
	python -m venv .venv
#####################################################################################
prepare/proto: ./sage/audio2face/proto/audio2face_pb2.py
./sage/audio2face/proto/audio2face_pb2.py: ./sage/audio2face/proto/audio2face.proto
	python -m grpc_tools.protoc -I=./ --python_out=./ --grpc_python_out=./ $^
#####################################################################################
install/req:
	# conda create --name sage python=3.10
	pip install -r requirements.txt
install/test-req:
	pip install -r requirements_test.txt

install/deps:
	sudo apt install -y portaudio19-dev python3-pyaudio

activate:
	source .venv/bin/activate
run:
	LOG_LEVEL=debug python -m sage.run --tts_key $(tts-key) \
	    --latex_url $(latex-url) \
	    --a2f_url=$(a2f-url) --a2f_name=$(a2f-name) \
	    --tts_url=$(tts-url) \
	    --kaldi_url=$(kaldi-url) $(usePCPlayer) $(greetOnConnect)

run/svg:
	docker run --rm -p 5030:5030 planqk/latex-renderer:v1.2.0

run/kaldi:
	docker run -it --rm -p 9090:80 intelektikalt/docker-kaldi-calc:0.1.1

run/fake-a2f:
	LOG_LEVEL=debug python -m sage.audio2face.samples.server

test:
	pytest -v --log-level=INFO

test/lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	#exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
#####################################################################################
.PHONY:
	run test prepare-env install-req
