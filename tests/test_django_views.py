import os


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mentor_service.settings",
)

import django  # noqa: E402
from django.test import Client, SimpleTestCase  # noqa: E402


django.setup()


class TestDjangoViews(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_homepage_opens(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сервис поиска наставников")

    def test_object_lists_open(self):
        for url in (
            "/mentors/",
            "/specializations/",
            "/applications/",
            "/users/",
        ):
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_dynamic_mentor_url_opens(self):
        response = self.client.get("/mentors/1/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Анна")

    def test_unknown_object_returns_404(self):
        response = self.client.get("/applications/999/")

        self.assertEqual(response.status_code, 404)
