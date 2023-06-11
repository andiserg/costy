class Limit:
    def __init__(
        self,
        user_id: int,
        category_id: int,
        limit: int,
        date_range: str,
        id: int | None = None,
    ):
        self.user_id = user_id
        self.category_id = (category_id,)
        self.limit = (limit,)
        self.date_range = date_range
        self.id = id
