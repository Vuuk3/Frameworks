from django.http import Http404

from app.models import User
from app.storage import load_objects
from web_common import cards, page


def _users() -> list[User]:
    return load_objects("users.json", User)


def user_list(request):
    """Show users without exposing their stored passwords."""
    blocks = [
        '<article class="card">'
        f"<h2>{item.name}</h2>"
        f'<p class="muted">{item.email}</p>'
        f'<a href="{item.id}/">Подробнее</a>'
        "</article>"
        for item in _users()
    ]
    content = "<h1>Пользователи</h1>" + cards(blocks)
    return page("Пользователи", content)


def user_detail(request, user_id: int):
    """Show one user selected through a dynamic URL."""
    user = next(
        (item for item in _users() if item.id == user_id),
        None,
    )
    if user is None:
        raise Http404("Пользователь не найден")
    content = (
        f"<h1>{user.name}</h1>"
        f"<p><strong>Email:</strong> {user.email}</p>"
        '<p><a href="/users/">Назад к списку</a></p>'
    )
    return page(user.name, content)
