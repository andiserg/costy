class User:
    def __init__(self, email: str, hashed_password: str, id: int = None):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
