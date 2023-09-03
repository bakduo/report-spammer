FROM python:3.10-slim as builder

RUN apt-get update && apt install -y libmagic1 python3-magic && cd /tmp/ && mkdir -p /home/app && useradd --shell /bin/bash --home-dir /home/app app && chown -R app:app /home/app

ENV PROJECT_DIR /home/app

WORKDIR ${PROJECT_DIR}

USER app

COPY --chown=app requirements.txt ${PROJECT_DIR}/

RUN export PATH=$PATH:/home/app/.local/bin && pip install -U pip --user && pip install -r /home/app/requirements.txt --user

FROM python:3.10-slim

LABEL org.opencontainers.image.authors="bakduo"

LABEL org.opencontainers.image.version="1.0.0"

LABEL org.opencontainers.image.licenses="GPL-3.0"

LABEL org.opencontainers.image.ref.name="spamapp"

LABEL description="Spam report for blacklist|grylist|reporting"

RUN mkdir -p /home/app && useradd --shell /bin/bash --home-dir /home/app app && chown -R app:app /home/app

ENV PROJECT_DIR /home/app

WORKDIR ${PROJECT_DIR}

USER app

COPY --chown=app --from=builder /home/app/.local /home/app/.local

COPY --chown=app . /home/app/

ENV PORT=8000

ENV PATH_APP=""

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

VOLUME ["/home/app/config","/home/app/static","/home/app/log"]