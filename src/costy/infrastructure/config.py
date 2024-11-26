import json
import logging
import os
from importlib import resources
from typing import Any


class SettingError(Exception):
    pass


def get_db_connection_url() -> str:
    user = _get_env_var("DB_USER")
    password = _get_env_var("DB_PASSWORD")
    host = _get_env_var("DB_HOST")
    port = _get_env_var("DB_PORT")
    db_name = _get_env_var("DB_NAME")
    schema = _get_env_var("DB_SCHEMA")

    return (
        f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"
        f"?options=-c search_path={schema}"
    )


def _get_env_var(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        raise SettingError(f'Environment variable "{name}" not exists')


def get_banks_conf() -> dict[str, Any]:
    with open(str(resources.files("costy.adapters.bankapi") / "_banks.json")) as f:
        return json.load(f)  # type: ignore[no-any-return]


def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s %(asctime)s %(levelname)s %(message)s",
    )
