set shell := ["sh", "-c"]

set dotenv-required
set dotenv-load := true

migrate:
    alembic upgrade head

docker-push:
    docker build . -t costy
    docker tag costy sergienkoandrew/costy
    docker push sergienkoandrew/costy
