class Operation:
    def __init__(
        self,
        amount: int,
        description: str | None,
        time: int,
        source_type: str,
        user_id: int,
        category_id: int | None = None,
        subcategory_id: int | None = None,
        id: int = None,
        **kwargs,
    ):
        self.amount = amount
        self.description = description
        self.time = time
        self.source_type = source_type
        self.user_id = user_id
        self.id = id
        self.category_id = category_id
        self.subcategory_id = subcategory_id
