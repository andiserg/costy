from pydantic import BaseModel


class StatisticSchema(BaseModel):
    """Схема операції. Модель: src.app.domain.unit.Statistic"""

    costs_sum: int
    most_popular_category: int
    categories_costs: dict[int, int]
