import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import mentors


class TestMentors(unittest.TestCase):

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

    def test_register_mentor(self):
        mentor = mentors.register_mentor(
            "Анна",
            "anna@test.ru",
            [1],
        )

        self.assertEqual(mentor.name, "Анна")
        self.assertEqual(mentor.email, "anna@test.ru")
        self.assertEqual(mentor.specializations, [1])


if __name__ == "__main__":
    unittest.main()
