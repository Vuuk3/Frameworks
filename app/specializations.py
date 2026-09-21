from .exceptions import SpecializationNotFoundError
from .models import Specialization
from .storage import get_next_id, load_objects, save_objects


SPECIALIZATIONS_FILE = "specializations.json"


def add_specialization(
    name: str,
    description: str = "",
) -> Specialization:
    """Добавить новую специализацию."""

    specializations = load_objects(SPECIALIZATIONS_FILE, Specialization)

    specialization = Specialization(
        id=get_next_id(specializations),
        name=name.strip(),
        description=description.strip(),
    )

    specializations.append(specialization)
    save_objects(SPECIALIZATIONS_FILE, specializations)

    return specialization


def get_specialization(specialization_id: int) -> Specialization:
    """Получить специализацию по ID."""

    specializations = load_objects(SPECIALIZATIONS_FILE, Specialization)

    for item in specializations:
        if item.id == specialization_id:
            return item

    raise SpecializationNotFoundError(
        f"Специализация с ID {specialization_id} не найдена."
    )


def get_all_specializations() -> list[Specialization]:
    """Получить все специализации."""

    return load_objects(SPECIALIZATIONS_FILE, Specialization)
