FROM python:3.11.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY . ./

RUN pip install -e . --default-timeout=100
