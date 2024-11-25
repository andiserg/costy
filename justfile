set shell := ["sh", "-c"]

set dotenv-required
set dotenv-load := true

docker-push:
    docker build . -t costy
    docker tag costy sergienkoandrew/costy
    docker push sergienkoandrew/costy

install service:
    cp pyproject_{{service}}.toml pyproject.toml
    uv sync --all-extras
    rm -f pyproject.toml

install-all:
    cp pyproject_costy.toml pyproject.toml
    uv sync --all-extras
    rm -f pyproject.toml

    cp pyproject_auth.toml pyproject.toml
    uv pip install -e .
    rm -f pyproject.toml
