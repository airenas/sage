FROM python:3.10-alpine3.16 as py_make
RUN apk add --no-cache --virtual .build-deps gcc musl-dev g++

FROM py_make as runner
RUN apk add --update --no-cache portaudio-dev py3-pyaudio ffmpeg
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps

FROM runner

ENV UID=999
RUN addgroup app && adduser -S -G app app --uid $UID app

ARG BUILD_VERSION=0.1

LABEL org.opencontainers.image.version=$BUILD_VERSION \
      org.opencontainers.image.authors="airenass@gmail.com" \
      name="roxy-inform" \
      maintainer="airenass@gmail.com" \
      vendor="airenass@gmail.com" \
      version=$BUILD_VERSION \
      release=$BUILD_VERSION \
      summary="This image is used to run sage service" \
      description="This image is used to run sage service" 

COPY ./sage /app/sage
COPY ./data /app/data

RUN chown app:app /app/* /app
USER app

CMD [ "-m", "sage.run", "--help" ]
ENTRYPOINT ["python"]