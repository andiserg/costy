set shell := ["sh", "-c"]

set dotenv-required
set dotenv-load := true

migrate:
    alembic upgrade head
