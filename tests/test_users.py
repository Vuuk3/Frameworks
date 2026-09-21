import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import users
from app.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.data_dir_patch = patch(
            "app.storage.DATA_DIR",
            Path(self.temp_dir.name),
        )
        self.data_dir_patch.start()

    def tearDown(self):
        self.data_dir_patch.stop()
        self.temp_dir.cleanup()

    def test_register_user(self):
        user = users.register_user(
            "Иван",
            "ivan@test.ru",
            "1234",
        )

        self.assertEqual(user.name, "Иван")
        self.assertEqual(user.email, "ivan@test.ru")

    def test_duplicate_email(self):
        users.register_user(
            "Иван",
            "duplicate@test.ru",
            "1234",
        )

        with self.assertRaises(UserAlreadyExistsError):
            users.register_user(
                "Пётр",
                "duplicate@test.ru",
                "5678",
            )

    def test_wrong_password(self):
        users.register_user(
            "Иван",
            "auth@test.ru",
            "1234",
        )

        with self.assertRaises(UserNotFoundError):
            users.authenticate_user(
                "auth@test.ru",
                "wrong",
            )


if __name__ == "__main__":
    unittest.main()
