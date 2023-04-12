class Manager:
    """Менеджер з'єднання з банком"""

    def __init__(self, bank_name: str, user_id: int, id: int = None):
        self.bank_name = bank_name
        self.user_id = user_id
        self.id = id


class ManagerProperty:
    """
    Потрібні поля для праці з менеджером.
    Реалізує EAV паттерн.
    """

    def __init__(
        self, name: str, value: str, value_type: str, manager_id: int, id: int = None
    ):
        self.name = name
        self.value = value
        self.type = value_type
        self.manager_id = manager_id
        self.id = id

    def as_dict(self):
        types = {"str": str, "int": int, "float": float}
        return {f"{self.name}": types[self.type](self.value)}
