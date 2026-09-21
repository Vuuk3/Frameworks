import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from app import applications, mentors
from app.exceptions import (
    ApplicationAlreadyExistsError,
    InvalidDataError,
)


class TestApplications(unittest.TestCase):

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

    def test_create_application(self):
        application = applications.create_application(1, 1)

        self.assertEqual(application.user_id, 1)
        self.assertEqual(application.specialization_id, 1)
        self.assertEqual(application.status, "open")

    def test_duplicate_application(self):
        applications.create_application(10, 10)

        with self.assertRaises(ApplicationAlreadyExistsError):
            applications.create_application(10, 10)

    def test_mentor_responds_to_application(self):
        mentor = mentors.register_mentor(
            "Анна",
            "anna@test.ru",
            [1],
        )
        application = applications.create_application(1, 1)

        accepted = applications.respond_to_application(
            application.id,
            mentor.id,
        )

        self.assertEqual(accepted.status, "accepted")
        self.assertEqual(accepted.mentor_id, mentor.id)

    def test_mentor_cannot_respond_for_other_specialization(self):
        mentor = mentors.register_mentor(
            "Анна",
            "anna@test.ru",
            [2],
        )
        application = applications.create_application(1, 1)

        with self.assertRaises(InvalidDataError):
            applications.respond_to_application(
                application.id,
                mentor.id,
            )


if __name__ == "__main__":
    unittest.main()
