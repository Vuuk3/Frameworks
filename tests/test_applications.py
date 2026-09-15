import unittest

from app.applications import create_application
from app.exceptions import ApplicationAlreadyExistsError


class TestApplications(unittest.TestCase):

    def test_create_application(self):
        application = create_application(1, 1)

        self.assertEqual(application.user_id, 1)
        self.assertEqual(application.specialization_id, 1)
        self.assertEqual(application.status, "open")

    def test_duplicate_application(self):
        create_application(10, 10)

        with self.assertRaises(ApplicationAlreadyExistsError):
            create_application(10, 10)


if __name__ == "__main__":
    unittest.main()