import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import specializations


class TestSpecializations(unittest.TestCase):

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

    def test_add_specialization(self):
        specialization = specializations.add_specialization(
            "Python",
            "Программирование на Python",
        )

        self.assertEqual(specialization.name, "Python")
        self.assertEqual(
            specialization.description,
            "Программирование на Python",
        )


if __name__ == "__main__":
    unittest.main()
