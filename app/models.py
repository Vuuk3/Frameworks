from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from .exceptions import InvalidDataError


class Entity(ABC):
    """Базовый класс сущностей сервиса."""

    def __init__(self, entity_id: int) -> None:
        if entity_id <= 0:
            raise InvalidDataError("ID должен быть положительным числом.")
        self.id = entity_id

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Преобразовать объект в словарь для сохранения в JSON."""

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict[str, Any]) -> Entity:
        """Создать объект из словаря, загруженного из JSON."""


class Person(Entity):
    """Общая модель участника сервиса."""

    def __init__(self, entity_id: int, name: str, email: str) -> None:
        super().__init__(entity_id)
        if not name.strip():
            raise InvalidDataError("Имя не может быть пустым.")
        if "@" not in email:
            raise InvalidDataError("Некорректный email.")

        self.name = name.strip()
        self._email = email.strip()

    @property
    def email(self) -> str:
        """Вернуть адрес электронной почты участника."""
        return self._email

    @abstractmethod
    def role(self) -> str:
        """Вернуть название роли участника."""


class User(Person):
    """Пользователь, который создаёт заявку на наставничество."""

    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        password: str,
    ) -> None:
        super().__init__(id, name, email)
        if len(password) < 4:
            raise InvalidDataError(
                "Пароль должен содержать минимум 4 символа."
            )
        self._password = password

    def role(self) -> str:
        return "пользователь"

    def check_password(self, password: str) -> bool:
        """Проверить пароль без раскрытия внутреннего атрибута."""
        return self._password == password

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self._password,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        return cls(**data)

    def __str__(self) -> str:
        return f"Пользователь {self.name} ({self.email})"


class Mentor(Person):
    """Наставник, работающий с заданными специализациями."""

    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        specializations: list[int],
    ) -> None:
        super().__init__(id, name, email)
        self._specializations = list(specializations)

    @property
    def specializations(self) -> list[int]:
        """Вернуть копию списка специализаций наставника."""
        return list(self._specializations)

    def role(self) -> str:
        return "наставник"

    def can_mentor(self, specialization: Specialization | int) -> bool:
        """Проверить, работает ли наставник со специализацией."""
        specialization_id = (
            specialization.id
            if isinstance(specialization, Specialization)
            else specialization
        )
        return specialization_id in self._specializations

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "specializations": self.specializations,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Mentor:
        return cls(**data)

    def __str__(self) -> str:
        return f"Наставник {self.name} ({self.email})"


class Specialization(Entity):
    """Направление, по которому пользователь ищет наставника."""

    def __init__(
        self,
        id: int,
        name: str,
        description: str = "",
    ) -> None:
        super().__init__(id)
        if not name.strip():
            raise InvalidDataError(
                "Название специализации не может быть пустым."
            )
        self.name = name.strip()
        self.description = description.strip()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Specialization:
        return cls(**data)

    def __str__(self) -> str:
        return self.name


class Application(Entity):
    """Заявка пользователя на подбор наставника."""

    def __init__(
        self,
        id: int,
        user_id: int,
        specialization_id: int,
        status: str = "open",
        mentor_id: int | None = None,
    ) -> None:
        super().__init__(id)
        if user_id <= 0 or specialization_id <= 0:
            raise InvalidDataError(
                "Некорректный ID пользователя или специализации."
            )
        self.user_id = user_id
        self.specialization_id = specialization_id
        self.status = status
        self.mentor_id = mentor_id

    def is_open(self) -> bool:
        """Проверить, открыта ли заявка."""
        return self.status == "open"

    def accept(self, mentor: Mentor) -> None:
        """Принять отклик подходящего наставника."""
        if not self.is_open():
            raise InvalidDataError("На эту заявку уже нельзя откликнуться.")
        if not mentor.can_mentor(self.specialization_id):
            raise InvalidDataError(
                "Наставник не работает с выбранной специализацией."
            )

        self.mentor_id = mentor.id
        self.status = "accepted"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "specialization_id": self.specialization_id,
            "status": self.status,
            "mentor_id": self.mentor_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Application:
        return cls(**data)

    def __str__(self) -> str:
        return (
            f"Заявка №{self.id}: пользователь {self.user_id}, "
            f"специализация {self.specialization_id}, статус {self.status}"
        )
