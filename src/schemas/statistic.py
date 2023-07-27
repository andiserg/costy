from pydantic import BaseModel


class StatisticSchema(BaseModel):
    """Схема операції. Модель: src.app.domain.unit.Statistic"""

    costs_sum: int
    categories_costs: dict[int | None, int]
    costs_num_by_days: dict[str, int]
    costs_sum_by_days: dict[str, int]
