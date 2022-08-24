-include Makefile.options
latex-url?=https://sinteze-test.intelektika.lt/latex-renderer/renderLatex
a2f-url?=localhost:50051
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
	pip install -r requirements.txt
install/test-req:
	pip install -r requirements_test.txt

install/deps:
	sudo apt install -y portaudio19-dev python3-pyaudio

activate:
	source .venv/bin/activate
run:
	LOG_LEVEL=debug python -m sage.run --tts_key $(tts-key) --latex_url $(latex-url) --a2f_url=$(a2f-url) \
	--a2f_name=$(a2f-name)
# 	--usePCPlayer

run/svg:
	docker run --rm -p 5030:5030 planqk/latex-renderer:v1.2.0

run/fake-a2f:
	LOG_LEVEL=debug python -m sage.audio2face.samples.server

test:
	pytest -v --log-level=INFO
#####################################################################################
.PHONY:
	run test prepare-env install-req
