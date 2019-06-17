from python:3.7.1-alpine3.8

COPY . /dialogapi

RUN pip install /dialogapi/

WORKDIR /workspace

ENTRYPOINT ["python", "-um", "dialogapi.main"]