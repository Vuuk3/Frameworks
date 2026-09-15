from .exceptions import MentorNotFoundError
from .models import Mentor
from .storage import get_next_id, load_data, save_data


MENTORS_FILE = "mentors.json"


def register_mentor(
    name: str,
    email: str,
    specializations: list[int],
) -> Mentor:
    """Зарегистрировать наставника."""

    mentors = load_data(MENTORS_FILE)

    mentor = Mentor(
        id=get_next_id(mentors),
        name=name.strip(),
        email=email.strip(),
        specializations=specializations,
    )

    mentors.append(mentor.to_dict())
    save_data(MENTORS_FILE, mentors)

    return mentor


def get_mentor(mentor_id: int) -> Mentor:
    """Получить наставника по ID."""

    mentors = load_data(MENTORS_FILE)

    for mentor in mentors:
        if mentor["id"] == mentor_id:
            return Mentor(**mentor)

    raise MentorNotFoundError(
        f"Наставник с ID {mentor_id} не найден."
    )


def get_mentors_by_specialization(
    specialization_id: int,
) -> list[Mentor]:
    """Найти наставников по специализации."""

    mentors = load_data(MENTORS_FILE)

    return [
        Mentor(**mentor)
        for mentor in mentors
        if specialization_id in mentor["specializations"]
    ]