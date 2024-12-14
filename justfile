set shell := ["sh", "-c"]

set dotenv-load := true

docker-push service:
    docker build conf/{{service}} -t {{service}}
    docker tag costy sergienkoandrew/costy:{{service}}
    docker push sergienkoandrew/costy:{{service}}

install service:
    mv pyproject.toml pyproject_tools.toml
    cp conf/{{service}}/pyproject.toml pyproject.toml
    uv sync --all-extras
    rm -f pyproject.toml
    mv pyproject_tools.toml pyproject.toml

install-all:
    mv pyproject.toml pyproject_tools.toml

    cp conf/costy/pyproject.toml pyproject.toml
    uv sync --all-extras
    rm -f pyproject.toml

    cp conf/auth/pyproject.toml pyproject.toml
    uv pip install -e .
    rm -f pyproject.toml
    mv pyproject_tools.toml pyproject.toml

install-ci service:
    mv pyproject.toml pyproject_tools.toml
    cp conf/{{service}}/pyproject.toml pyproject.toml
    uv sync --extra ci
    rm -f pyproject.toml
    mv pyproject_tools.toml pyproject.toml

ci-tests service:
    mv pyproject.toml pyproject_tools.toml
    cp conf/{{service}}/pyproject.toml pyproject.toml
    uv run coverage run --source=src/{{service}} -m pytest
    rm -f pyproject.toml
    mv pyproject_tools.toml pyproject.toml
