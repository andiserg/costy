FROM python:3.12-bookworm AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ADD . /app

RUN --mount=type=bind,source=conf/costy/pyproject.toml,target=pyproject.toml \
    uv lock

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=conf/costy/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable

RUN --mount=type=bind,source=conf/costy/pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-editable


FROM python:3.12-bookworm

COPY --from=builder --chown=app:app /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
