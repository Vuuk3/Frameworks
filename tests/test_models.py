import unittest

from app.models import Application, Mentor, Person, User


class TestModels(unittest.TestCase):

    def test_person_inheritance_and_polymorphism(self):
        people = [
            User(1, "Иван", "ivan@test.ru", "1234"),
            Mentor(2, "Анна", "anna@test.ru", [1]),
        ]

        self.assertTrue(all(isinstance(person, Person) for person in people))
        self.assertEqual(
            [person.role() for person in people],
            ["пользователь", "наставник"],
        )

    def test_string_representation(self):
        user = User(1, "Иван", "ivan@test.ru", "1234")

        self.assertEqual(
            str(user),
            "Пользователь Иван (ivan@test.ru)",
        )

    def test_objects_interact(self):
        mentor = Mentor(1, "Анна", "anna@test.ru", [3])
        application = Application(1, 2, 3)

        application.accept(mentor)

        self.assertEqual(application.status, "accepted")
        self.assertEqual(application.mentor_id, mentor.id)


if __name__ == "__main__":
    unittest.main()
