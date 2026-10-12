from app.models import Application, Mentor, Specialization, User
from app.storage import load_objects
from django.shortcuts import render


def index(request):
    """Show the project homepage and current JSON record counts."""
    sections = (
        {
            "label": "Наставники",
            "count": len(load_objects("mentors.json", Mentor)),
            "url_name": "mentors:list",
        },
        {
            "label": "Специализации",
            "count": len(
                load_objects("specializations.json", Specialization)
            ),
            "url_name": "specializations:list",
        },
        {
            "label": "Заявки",
            "count": len(load_objects("applications.json", Application)),
            "url_name": "applications:list",
        },
        {
            "label": "Пользователи",
            "count": len(load_objects("users.json", User)),
            "url_name": "users:list",
        },
    )
    return render(request, "homepage/index.html", {"sections": sections})


def page_not_found(request, exception):
    """Return the project-specific page for missing routes and objects."""
    return render(request, "404.html", status=404)
