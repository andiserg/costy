class Category:
    id: int | None
    name: str
    user_id: int | None

    def __init__(self, name: str, user_id: int | None, id: int | None = None):
        self.id = id
        self.name = name
        self.user_id = user_id
