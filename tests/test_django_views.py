import os
from unittest.mock import patch


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "mentor_service.settings",
)

import django  # noqa: E402
from django.contrib.staticfiles import finders  # noqa: E402
from django.test import Client, SimpleTestCase  # noqa: E402
from django.test import override_settings  # noqa: E402
from django.test.utils import setup_test_environment  # noqa: E402
from django.urls import reverse  # noqa: E402


django.setup()
setup_test_environment()


class TestDjangoViews(SimpleTestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_homepage_opens(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сервис поиска наставников")
        self.assertContains(response, "bootstrap@5.3.3")
        self.assertTemplateUsed(response, "homepage/index.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "includes/navigation.html")

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
        response = self.client.get(reverse("mentors:detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Анна")
        self.assertTemplateUsed(response, "mentors/mentor_detail.html")

    def test_lists_use_templates_and_named_urls(self):
        expected = (
            ("mentors:list", "mentors/mentor_list.html"),
            (
                "specializations:list",
                "specializations/specialization_list.html",
            ),
            (
                "applications:list",
                "applications/application_list.html",
            ),
            ("users:list", "users/user_list.html"),
        )
        for url_name, template_name in expected:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template_name)
                self.assertTemplateUsed(response, "base.html")

    @patch("mentors_site.views._mentors", return_value=[])
    def test_empty_mentor_list_is_explained(self, _mock_mentors):
        response = self.client.get(reverse("mentors:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Наставники пока не добавлены")

    def test_project_static_files_exist(self):
        for path in (
            "homepage/css/style.css",
            "homepage/js/main.js",
            "homepage/images/logo.svg",
        ):
            with self.subTest(path=path):
                self.assertIsNotNone(finders.find(path))

    def test_all_detail_pages_open(self):
        urls = (
            reverse("mentors:detail", args=[1]),
            reverse("specializations:detail", args=[1]),
            reverse("applications:detail", args=[1]),
            reverse("users:detail", args=[1]),
        )
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_application_status_condition(self):
        open_response = self.client.get(
            reverse("applications:detail", args=[1])
        )
        accepted_response = self.client.get(
            reverse("applications:detail", args=[3])
        )

        self.assertContains(open_response, "Открыта")
        self.assertContains(accepted_response, "Принята")

    def test_navigation_contains_named_routes(self):
        response = self.client.get(reverse("homepage:index"))

        for url_name in (
            "homepage:index",
            "mentors:list",
            "specializations:list",
            "applications:list",
            "users:list",
        ):
            with self.subTest(url_name=url_name):
                self.assertContains(response, f'href="{reverse(url_name)}"')

    def test_page_references_project_static_files(self):
        response = self.client.get(reverse("homepage:index"))

        self.assertContains(response, "/static/homepage/css/style.css")
        self.assertContains(response, "/static/homepage/js/main.js")
        self.assertContains(response, "/static/homepage/images/logo.svg")

    def test_unknown_object_returns_404(self):
        response = self.client.get("/applications/999/")

        self.assertEqual(response.status_code, 404)

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/missing-page/")

        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "Страница не найдена",
            status_code=404,
        )
