class Manager:
    """Менеджер з'єднання з банком"""

    bank_name: str
    updated_time: int
    user_id: int


class ManagerProperty:
    """
    Потрібні поля для праці з менеджером.
    Реалізує EAV паттерн.
    """

    name: str
    value: str
    type: int  # str | int | float
    manager_id: int

    def as_dict(self):
        types = {"str": str, "int": int, "float": float}
        return {
            "name": self.name,
            "value": types[self.type](self.value),
        }
