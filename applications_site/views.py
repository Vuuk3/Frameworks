from django.http import Http404

from app.models import Application, Mentor, Specialization, User
from app.storage import load_objects
from web_common import cards, page


def _applications() -> list[Application]:
    return load_objects("applications.json", Application)


def _related_data():
    users = {
        item.id: item
        for item in load_objects("users.json", User)
    }
    mentors = {
        item.id: item
        for item in load_objects("mentors.json", Mentor)
    }
    specializations = {
        item.id: item
        for item in load_objects(
            "specializations.json",
            Specialization,
        )
    }
    return users, mentors, specializations


def application_list(request):
    """Show applications with names resolved from related objects."""
    users, mentors, specializations = _related_data()
    blocks = []
    for item in _applications():
        user = users.get(item.user_id)
        specialization = specializations.get(item.specialization_id)
        user_name = (
            user.name
            if user
            else f"Пользователь №{item.user_id}"
        )
        specialization_name = (
            specialization.name
            if specialization
            else f"Специализация №{item.specialization_id}"
        )
        blocks.append(
            '<article class="card">'
            f"<h2>Заявка №{item.id}</h2>"
            f"<p>{user_name}</p>"
            "<p class=\"muted\">"
            f"{specialization_name}"
            "</p>"
            f'<p class="status">{item.status}</p>'
            f'<a href="{item.id}/">Подробнее</a>'
            "</article>"
        )
    content = "<h1>Заявки</h1>" + cards(blocks)
    return page("Заявки", content)


def application_detail(request, application_id: int):
    """Show one application selected through a dynamic URL."""
    application = next(
        (
            item
            for item in _applications()
            if item.id == application_id
        ),
        None,
    )
    if application is None:
        raise Http404("Заявка не найдена")

    users, mentors, specializations = _related_data()
    user = users.get(application.user_id)
    mentor = mentors.get(application.mentor_id)
    specialization = specializations.get(application.specialization_id)
    specialization_name = (
        specialization.name
        if specialization
        else f"№{application.specialization_id}"
    )
    content = (
        f"<h1>Заявка №{application.id}</h1>"
        "<p><strong>Пользователь:</strong> "
        f"{user.name if user else '№' + str(application.user_id)}</p>"
        "<p><strong>Специализация:</strong> "
        f"{specialization_name}</p>"
        f"<p><strong>Статус:</strong> {application.status}</p>"
        "<p><strong>Наставник:</strong> "
        f"{mentor.name if mentor else 'Не назначен'}</p>"
        '<p><a href="/applications/">Назад к списку</a></p>'
    )
    return page(f"Заявка №{application.id}", content)
