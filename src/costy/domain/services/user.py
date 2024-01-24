from costy.domain.models.user import User


class UserService:
    def create(self, email: str, hashed_password: str) -> User:
        return User(id=None, email=email, hashed_password=hashed_password)
