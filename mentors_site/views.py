from django.http import Http404

from app.models import Mentor, Specialization
from app.storage import load_objects
from web_common import cards, page


def _mentors() -> list[Mentor]:
    return load_objects("mentors.json", Mentor)


def _specialization_names() -> dict[int, str]:
    items = load_objects("specializations.json", Specialization)
    return {item.id: item.name for item in items}


def mentor_list(request):
    """Show all mentors stored by the console application."""
    names = _specialization_names()
    blocks = []
    for mentor in _mentors():
        labels = [
            names.get(item, f"№{item}")
            for item in mentor.specializations
        ]
        blocks.append(
            '<article class="card">'
            f"<h2>{mentor.name}</h2>"
            f'<p class="muted">{", ".join(labels) or "Не указаны"}</p>'
            f'<a href="{mentor.id}/">Подробнее</a>'
            "</article>"
        )
    content = "<h1>Наставники</h1>" + cards(blocks)
    return page("Наставники", content)


def mentor_detail(request, mentor_id: int):
    """Show one mentor selected through a dynamic URL."""
    mentor = next(
        (item for item in _mentors() if item.id == mentor_id),
        None,
    )
    if mentor is None:
        raise Http404("Наставник не найден")

    names = _specialization_names()
    labels = [
        names.get(item, f"№{item}")
        for item in mentor.specializations
    ]
    content = (
        f"<h1>{mentor.name}</h1>"
        f"<p><strong>Email:</strong> {mentor.email}</p>"
        "<p><strong>Специализации:</strong> "
        f"{', '.join(labels) or 'Не указаны'}</p>"
        '<p><a href="/mentors/">Назад к списку</a></p>'
    )
    return page(mentor.name, content)
