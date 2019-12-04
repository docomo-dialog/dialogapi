from 3.6.9-alpine3.10

COPY . /dialogapi

RUN pip install /dialogapi/

WORKDIR /workspace

ENTRYPOINT ["python", "-um", "dialogapi.main"]