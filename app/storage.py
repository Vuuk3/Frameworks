import json
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def _get_path(filename: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    return DATA_DIR / filename


def load_data(filename: str) -> list:
    """Загрузить список объектов из JSON-файла."""
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


def save_data(filename: str, data: list) -> None:
    """Сохранить список объектов в JSON-файл."""
    path = _get_path(filename)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def get_next_id(data: list) -> int:
    """Получить следующий свободный ID."""
    if not data:
        return 1

    return max(item["id"] for item in data) + 1