from dataclasses import dataclass


@dataclass
class Statistic:
    costs_sum: int
    categories_costs: dict[int, int]
