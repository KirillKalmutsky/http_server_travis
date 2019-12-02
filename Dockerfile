FROM python:3.7.2-alpine3.8

COPY server.py /
COPY docker-compose.yaml /

RUN apk update && apk upgrade && apk add bash

EXPOSE 65432

ENTRYPOINT ["python", "server.py"]