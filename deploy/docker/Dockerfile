FROM python:3.10-slim

ENV PYTHONPATH "${PYTHONPATH}:/patent_fetcher:/patent_fetcher/src:/patent_fetcher/venv"

COPY . /patent_fetcher/
WORKDIR /patent_fetcher

RUN apt-get update && \
    apt-get install -y \
    gcc curl

RUN pip install --upgrade pip \
    && pip install poetry

RUN adduser -u 1000 --gecos "" --disabled-password patents \
    && mkdir /venv \
    && chown -R patents:patents /venv \
    && chown -R patents:patents /patent_fetcher \
    && . venv/bin/activate \

USER patents

RUN POETRY_VIRTUALENVS_CREATE=false poetry install --no-ansi