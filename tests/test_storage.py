import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app.models import User
from app.storage import load_objects, save_objects


class TestStorage(unittest.TestCase):

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

    def test_object_json_round_trip(self):
        users = [User(1, "Иван", "ivan@test.ru", "1234")]

        save_objects("users.json", users)
        loaded_users = load_objects("users.json", User)

        self.assertEqual(len(loaded_users), 1)
        self.assertIsInstance(loaded_users[0], User)
        self.assertEqual(loaded_users[0].email, "ivan@test.ru")
        self.assertTrue(loaded_users[0].check_password("1234"))


if __name__ == "__main__":
    unittest.main()
