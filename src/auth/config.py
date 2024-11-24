import os
from dataclasses import dataclass


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
    user = _get_env_var("DB_USER")
    password = _get_env_var("DB_PASSWORD")
    host = _get_env_var("DB_HOST")
    port = _get_env_var("DB_PORT")
    db_name = _get_env_var("DB_NAME")

    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"


def _get_env_var(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        raise SettingError(f'Environment variable "{name}" not exists')
