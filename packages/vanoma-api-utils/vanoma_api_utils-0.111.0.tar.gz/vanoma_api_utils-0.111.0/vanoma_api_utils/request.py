from typing import Any, Dict


def stringify_filters(filters: Dict[str, Any]) -> str:
    return "&".join(map(lambda item: f"{item[0]}={item[1]}", filters.items()))
