import os

env_file = os.getenv("GITHUB_ENV", False)
if env_file:
    with open(env_file, "r") as f:
        print(f.read())
print(os.getenv("DB_USER"))
print(os.getenv("DB_PASSWORD"))
print(os.getenv("TEST_DB_NAME"))
print(os.getenv("DB_HOST"))
