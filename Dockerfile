FROM python:3.8-slim

LABEL maintainer="bakdou"

ENV PYTHONBUFFERED 1

ENV PYTHONWRITEBYTECODE 1

RUN apt-get update && apt-get install -y netcat && cd /tmp/ && pip install -U pip && mkdir -p /home/app /home/app/staticfiles && useradd --shell /bin/bash --home-dir /home/app app && chown -R app:app /home/app

ENV PROJECT_DIR /home/app

WORKDIR ${PROJECT_DIR}

USER app

COPY Pipfile* ${PROJECT_DIR}/

RUN export PATH=$PATH:/home/app/.local/bin && pip install pipenv && pipenv lock --keep-outdated --requirements > /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY . ${PROJECT_DIR}/

USER root

RUN chown -R app:app ${PROJECT_DIR}/

USER app

VOLUME ["/home/app/config"]

ENTRYPOINT ["/home/app/entrypoint.sh"]
