from .exceptions import (
    ApplicationAlreadyExistsError,
    ApplicationNotFoundError,
    InvalidDataError,
)
from .models import Application
from .storage import get_next_id, load_data, save_data


APPLICATIONS_FILE = "applications.json"


def create_application(
    user_id: int,
    specialization_id: int,
) -> Application:
    """Создать заявку пользователя."""

    if user_id <= 0 or specialization_id <= 0:
        raise InvalidDataError("Некорректный ID пользователя или специализации.")

    applications = load_data(APPLICATIONS_FILE)

    for application in applications:
        if (
            application["user_id"] == user_id
            and application["specialization_id"] == specialization_id
            and application["status"] == "open"
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

    applications.append(application.to_dict())
    save_data(APPLICATIONS_FILE, applications)

    return application


def get_open_applications() -> list[Application]:
    """Получить все открытые заявки."""

    applications = load_data(APPLICATIONS_FILE)

    return [
        Application(**application)
        for application in applications
        if application["status"] == "open"
    ]


def respond_to_application(
    application_id: int,
    mentor_id: int,
) -> Application:
    """Наставник откликается на заявку."""

    applications = load_data(APPLICATIONS_FILE)

    for application in applications:
        if application["id"] == application_id:

            if application["status"] != "open":
                raise InvalidDataError(
                    "На эту заявку уже нельзя откликнуться."
                )

            application["mentor_id"] = mentor_id
            application["status"] = "accepted"

            save_data(APPLICATIONS_FILE, applications)

            return Application(**application)

    raise ApplicationNotFoundError(
        f"Заявка с ID {application_id} не найдена."
    )


def get_application(application_id: int) -> Application:
    """Получить заявку по ID."""

    applications = load_data(APPLICATIONS_FILE)

    for application in applications:
        if application["id"] == application_id:
            return Application(**application)

    raise ApplicationNotFoundError(
        f"Заявка с ID {application_id} не найдена."
    )