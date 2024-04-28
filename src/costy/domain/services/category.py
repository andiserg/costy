from costy.domain.models.category import Category, CategoryType
from costy.domain.models.user import UserId
from costy.domain.sentinel import Sentinel, SentinelOptional


class CategoryService:
    def create(
        self,
        name: str,
        kind: CategoryType,
        user_id: UserId,
        view: dict | None,
    ) -> Category:
        return Category(id=None, name=name, kind=kind.value, user_id=user_id, view=view)

    def update(
        self,
        category: Category,
        name: str | None,
        view: SentinelOptional[dict],
    ) -> None:
        if name:
            category.name = name
        if view is not Sentinel:
            category.view = view  # type: ignore[assignment]
