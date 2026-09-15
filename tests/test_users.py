import unittest

from app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.users import authenticate_user, register_user


class TestUsers(unittest.TestCase):

    def test_register_user(self):
        user = register_user(
            "Иван",
            "ivan@test.ru",
            "1234",
        )

        self.assertEqual(user.name, "Иван")
        self.assertEqual(user.email, "ivan@test.ru")

    def test_duplicate_email(self):
        register_user(
            "Иван",
            "duplicate@test.ru",
            "1234",
        )

        with self.assertRaises(UserAlreadyExistsError):
            register_user(
                "Пётр",
                "duplicate@test.ru",
                "5678",
            )

    def test_wrong_password(self):
        register_user(
            "Иван",
            "auth@test.ru",
            "1234",
        )

        with self.assertRaises(UserNotFoundError):
            authenticate_user(
                "auth@test.ru",
                "wrong",
            )


if __name__ == "__main__":
    unittest.main()