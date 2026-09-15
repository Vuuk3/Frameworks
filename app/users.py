from .exceptions import (
    InvalidDataError,
    UserAlreadyExistsError,
    UserNotFoundError,
)
from .models import User
from .storage import get_next_id, load_data, save_data


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

    users = load_data(USERS_FILE)

    if any(user["email"] == email for user in users):
        raise UserAlreadyExistsError(
            "Пользователь с таким email уже существует."
        )

    user = User(
        id=get_next_id(users),
        name=name.strip(),
        email=email.strip(),
        password=password,
    )

    users.append(user.to_dict())
    save_data(USERS_FILE, users)

    return user


def get_user(user_id: int) -> User:
    """Получить пользователя по ID."""

    users = load_data(USERS_FILE)

    for user in users:
        if user["id"] == user_id:
            return User(**user)

    raise UserNotFoundError(f"Пользователь с ID {user_id} не найден.")


def authenticate_user(email: str, password: str) -> User:
    """Авторизация пользователя."""

    users = load_data(USERS_FILE)

    for user in users:
        if user["email"] == email and user["password"] == password:
            return User(**user)

    raise UserNotFoundError("Неверный email или пароль.")