from .exceptions import (
    InvalidDataError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from .models import User
from .storage import get_next_id, load_objects, save_objects


USERS_FILE = "users.json"


def register_user(name: str, email: str, password: str) -> User:
    """Зарегистрировать нового пользователя."""

    if not name.strip():
        raise InvalidDataError("Имя не может быть пустым.")

    if "@" not in email:
        raise InvalidDataError("Некорректный email.")

    if len(password) < 4:
        raise InvalidDataError(
            "Пароль должен содержать минимум 4 символа."
        )

    users = load_objects(USERS_FILE, User)

    if any(user.email == email.strip() for user in users):
        raise UserAlreadyExistsError(
            "Пользователь с таким email уже существует."
        )

    user = User(
        id=get_next_id(users),
        name=name.strip(),
        email=email.strip(),
        password=password,
    )

    users.append(user)
    save_objects(USERS_FILE, users)

    return user


def get_user(user_id: int) -> User:
    """Получить пользователя по ID."""

    users = load_objects(USERS_FILE, User)

    for user in users:
        if user.id == user_id:
            return user

    raise UserNotFoundError(f"Пользователь с ID {user_id} не найден.")


def authenticate_user(email: str, password: str) -> User:
    """Авторизация пользователя."""

    users = load_objects(USERS_FILE, User)

    for user in users:
        if user.email == email and user.check_password(password):
            return user

    raise UserNotFoundError("Неверный email или пароль.")
