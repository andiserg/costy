class Category:
    id: int | None
    name: str
    user_id: int | None
    type: str
    icon_name: str | None
    icon_color: str | None

    def __init__(
        self,
        name: str,
        user_id: int | None,
        type: str,
        id: int | None = None,
        icon_name: str | None = None,
        icon_color: str | None = None,
        parent_id: int | None = None,
    ):
        self.id = id
        self.name = name
        self.user_id = user_id
        self.type = type
        self.icon_name = icon_name
        self.icon_color = icon_color
        self.parent_id = parent_id
