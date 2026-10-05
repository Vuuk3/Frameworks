from django.http import Http404

from app.models import Specialization
from app.storage import load_objects
from web_common import cards, page


def _specializations() -> list[Specialization]:
    return load_objects("specializations.json", Specialization)


def specialization_list(request):
    """Show all available learning directions."""
    blocks = [
        '<article class="card">'
        f"<h2>{item.name}</h2>"
        f'<p class="muted">{item.description}</p>'
        f'<a href="{item.id}/">Подробнее</a>'
        "</article>"
        for item in _specializations()
    ]
    content = "<h1>Специализации</h1>" + cards(blocks)
    return page("Специализации", content)


def specialization_detail(request, specialization_id: int):
    """Show one specialization selected through a dynamic URL."""
    item = next(
        (
            specialization
            for specialization in _specializations()
            if specialization.id == specialization_id
        ),
        None,
    )
    if item is None:
        raise Http404("Специализация не найдена")
    content = (
        f"<h1>{item.name}</h1>"
        f"<p>{item.description or 'Описание пока не добавлено.'}</p>"
        '<p><a href="/specializations/">Назад к списку</a></p>'
    )
    return page(item.name, content)
