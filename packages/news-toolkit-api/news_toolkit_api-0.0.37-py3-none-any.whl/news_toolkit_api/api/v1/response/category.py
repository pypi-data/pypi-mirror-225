from dataclasses import dataclass


@dataclass(frozen=True)
class CategoriesResponse:
    categories: list[str]
