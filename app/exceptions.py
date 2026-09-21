class ServiceError(Exception):
    """Базовое исключение сервиса."""


class UserAlreadyExistsError(ServiceError):
    """Пользователь уже существует."""


class UserNotFoundError(ServiceError):
    """Пользователь не найден."""


class MentorNotFoundError(ServiceError):
    """Наставник не найден."""


class SpecializationNotFoundError(ServiceError):
    """Специализация не найдена."""


class ApplicationNotFoundError(ServiceError):
    """Заявка не найдена."""


class InvalidDataError(ServiceError):
    """Некорректные данные."""


class ApplicationAlreadyExistsError(ServiceError):
    """Пользователь уже оставлял заявку на эту специализацию."""
