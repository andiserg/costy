from dataclasses import dataclass


@dataclass
class Statistic:
    costs_sum: int
    most_popular_category: int
    categories_costs: dict[int, int]
