import os


def get_db_connection_url() -> str:
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')

    if not all([user, password, host, port, db_name]):
        raise Exception("Database credentials not exists")
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"
