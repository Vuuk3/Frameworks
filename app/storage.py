import json
from pathlib import Path
from typing import Any, TypeVar

from .models import Entity


DATA_DIR = Path(__file__).parent.parent / "data"
ModelT = TypeVar("ModelT", bound=Entity)


def _get_path(filename: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR / filename


def load_data(filename: str) -> list[dict[str, Any]]:
    """Загрузить список словарей из JSON-файла."""
    path = _get_path(filename)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список")

        return data

    except json.JSONDecodeError as error:
        raise ValueError(f"Ошибка чтения JSON-файла: {filename}") from error


def save_data(filename: str, data: list[dict[str, Any]]) -> None:
    """Сохранить список словарей в JSON-файл."""
    path = _get_path(filename)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_objects(filename: str, model: type[ModelT]) -> list[ModelT]:
    """Загрузить JSON-данные как объекты указанного класса."""
    return [model.from_dict(item) for item in load_data(filename)]


def save_objects(filename: str, objects: list[Entity]) -> None:
    """Сохранить коллекцию объектов в JSON-файл."""
    save_data(filename, [item.to_dict() for item in objects])


def get_next_id(data: list[Entity] | list[dict[str, Any]]) -> int:
    """Получить следующий свободный ID."""
    if not data:
        return 1

    return max(
        item.id if isinstance(item, Entity) else item["id"]
        for item in data
    ) + 1
