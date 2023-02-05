import os

env_file = os.getenv("GITHUB_ENV", False)
if env_file:
    with open(env_file, "r") as f:
        print(f.read())
