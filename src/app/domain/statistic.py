from dataclasses import dataclass


@dataclass
class Statistic:
    costs_sum: int
    categories_costs: dict[int, int]
    costs_num_by_days: dict[str, int]
    costs_sum_by_days: dict[str, int]
