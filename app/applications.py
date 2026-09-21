from .exceptions import (
    ApplicationAlreadyExistsError,
    ApplicationNotFoundError,
    InvalidDataError,
    MentorNotFoundError,
)
from .models import Application, Mentor
from .storage import get_next_id, load_objects, save_objects


APPLICATIONS_FILE = "applications.json"
MENTORS_FILE = "mentors.json"


def create_application(
    user_id: int,
    specialization_id: int,
) -> Application:
    """Создать заявку пользователя."""

    if user_id <= 0 or specialization_id <= 0:
        raise InvalidDataError(
            "Некорректный ID пользователя или специализации."
        )

    applications = load_objects(APPLICATIONS_FILE, Application)

    for application in applications:
        if (
            application.user_id == user_id
            and application.specialization_id == specialization_id
            and application.is_open()
        ):
            raise ApplicationAlreadyExistsError(
                "У пользователя уже есть открытая заявка "
                "на эту специализацию."
            )

    application = Application(
        id=get_next_id(applications),
        user_id=user_id,
        specialization_id=specialization_id,
    )

    applications.append(application)
    save_objects(APPLICATIONS_FILE, applications)

    return application


def get_open_applications() -> list[Application]:
    """Получить все открытые заявки."""

    applications = load_objects(APPLICATIONS_FILE, Application)

    return [
        application
        for application in applications
        if application.is_open()
    ]


def respond_to_application(
    application_id: int,
    mentor_id: int,
) -> Application:
    """Наставник откликается на заявку."""

    applications = load_objects(APPLICATIONS_FILE, Application)
    mentors = load_objects(MENTORS_FILE, Mentor)

    mentor = next(
        (item for item in mentors if item.id == mentor_id),
        None,
    )
    if mentor is None:
        raise MentorNotFoundError(
            f"Наставник с ID {mentor_id} не найден."
        )

    for application in applications:
        if application.id == application_id:
            application.accept(mentor)
            save_objects(APPLICATIONS_FILE, applications)
            return application

    raise ApplicationNotFoundError(
        f"Заявка с ID {application_id} не найдена."
    )


def get_application(application_id: int) -> Application:
    """Получить заявку по ID."""

    applications = load_objects(APPLICATIONS_FILE, Application)

    for application in applications:
        if application.id == application_id:
            return application

    raise ApplicationNotFoundError(
        f"Заявка с ID {application_id} не найдена."
    )
