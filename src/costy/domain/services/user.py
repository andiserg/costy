from costy.domain.models.user import User


class UserService:
    def create(self, auth_id: str) -> User:
        return User(id=None, auth_id=auth_id)
