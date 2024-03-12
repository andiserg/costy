import json
import os
from dataclasses import dataclass
from importlib import resources
from typing import Any


class SettingError(Exception):
    pass


@dataclass
class AuthSettings:
    authorize_url: str
    register_url: str
    client_id: str
    client_secret: str
    audience: str
    grant_type: str
    issuer: str
    jwks_uri: str
    connection: str


def get_db_connection_url() -> str:
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    if not all([user, password, host, port, db_name]):
        raise Exception("Database credentials not exists")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


def get_auth_settings() -> AuthSettings:
    return AuthSettings(
        authorize_url=_get_env_var("AUTH0_AUTHORIZE_URL"),
        register_url=_get_env_var("AUTH0_REGISTER_URL"),
        grant_type="password",
        client_id=_get_env_var("AUTH0_CLIENT_ID"),
        client_secret=_get_env_var("AUTH0_CLIENT_SECRET"),
        audience=_get_env_var("AUTH0_AUDIENCE"),
        issuer=_get_env_var("AUTH0_ISSUER"),
        jwks_uri=_get_env_var("AUTH0_JWKS_URI"),
        connection=_get_env_var("AUTH0_CONNECTION")
    )


def _get_env_var(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        raise SettingError(f'Environment variable "{name}" not exists')


def get_banks_conf() -> dict[str, Any]:
    with open(str(resources.files("costy.adapters.bankapi") / "_banks.json"), "r") as f:
        confs = json.load(f)
    return confs
