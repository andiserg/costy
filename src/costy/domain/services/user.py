from costy.domain.models.user import User


class UserService:
    def create(self) -> User:
        return User(id=None)
