from app.models import Application, Mentor, Specialization, User
from app.storage import load_objects
from web_common import cards, page


def index(request):
    """Show the project homepage and current JSON record counts."""
    totals = (
        ("Наставники", "mentors.json", Mentor, "/mentors/"),
        (
            "Специализации",
            "specializations.json",
            Specialization,
            "/specializations/",
        ),
        (
            "Заявки",
            "applications.json",
            Application,
            "/applications/",
        ),
        ("Пользователи", "users.json", User, "/users/"),
    )
    blocks = []
    for label, filename, model, url in totals:
        count = len(load_objects(filename, model))
        blocks.append(
            '<section class="card">'
            f"<h2>{label}</h2>"
            f'<p class="muted">Записей: {count}</p>'
            f'<a href="{url}">Открыть раздел</a>'
            "</section>"
        )

    content = (
        "<h1>Сервис поиска наставников</h1>"
        "<p>Веб-интерфейс для просмотра наставников, направлений "
        "обучения и заявок пользователей.</p>"
        + cards(blocks)
    )
    return page("Сервис поиска наставников", content)
