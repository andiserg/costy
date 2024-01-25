from costy.domain.models.category import Category, CategoryType
from costy.domain.models.user import UserId


class CategoryService:
    def create(
        self, name: str, kind: CategoryType, user_id: UserId
    ) -> Category:
        return Category(id=None, name=name, kind=kind, user_id=user_id)
