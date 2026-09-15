from app.applications import (
    create_application,
    get_open_applications,
    respond_to_application,
)
from app.exceptions import ServiceError
from app.mentors import register_mentor
from app.specializations import add_specialization
from app.users import register_user


def main():
    try:
        user = register_user(
            "Иван",
            "ivan@example.com",
            "1234",
        )

        specialization = add_specialization(
            "Python",
            "Программирование на Python",
        )

        mentor = register_mentor(
            "Анна",
            "anna@example.com",
            [specialization.id],
        )

        application = create_application(
            user.id,
            specialization.id,
        )

        print("Пользователь:", user)
        print("Наставник:", mentor)
        print("Специализация:", specialization)
        print("Заявка:", application)

        response = respond_to_application(
            application.id,
            mentor.id,
        )

        print("Заявка после отклика:", response)

        print("\nОткрытые заявки:")
        for item in get_open_applications():
            print(item)

    except ServiceError as error:
        print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()