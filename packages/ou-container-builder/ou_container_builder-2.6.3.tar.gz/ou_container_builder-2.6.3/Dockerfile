FROM docker:20.10

RUN apk add --update --no-cache python3 python3-dev curl && \
    python3 -m ensurepip && \
    pip3 install --no-cache --upgrade pip

COPY dist/*.whl /tmp/source/

RUN cd /tmp/source && \
    python3 -m pip install /tmp/source/*.whl
