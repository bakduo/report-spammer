FROM python:3.11-slim as builder

RUN apt-get update && cd /tmp/ && pip install -U pip && mkdir -p /home/app /home/app/staticfiles && useradd --shell /bin/bash --home-dir /home/app app && chown -R app:app /home/app

ENV PROJECT_DIR /home/app

WORKDIR ${PROJECT_DIR}

USER app

COPY requirements.txt ${PROJECT_DIR}/

RUN export PATH=$PATH:/home/app/.local/bin && pip install -r /home/app/requirements.txt --user

FROM python:3.11-slim

LABEL org.opencontainers.image.authors="bakduo"

LABEL org.opencontainers.image.version="1.0.0"

LABEL org.opencontainers.image.licenses="GPL-3.0"

LABEL org.opencontainers.image.ref.name="spamapp"

LABEL description="Spam report for blacklist|grylist|reporting"

RUN mkdir -p /home/app /home/app/static && useradd --shell /bin/bash --home-dir /home/app app && chown -R app:app /home/app

ENV PROJECT_DIR /home/app

WORKDIR ${PROJECT_DIR}

USER app

COPY --from=builder /home/app/.local /home/app/.local

COPY . /home/app/

ENV PORT=8000

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

VOLUME ["/home/app/config","/home/app/static","/home/app/log"]