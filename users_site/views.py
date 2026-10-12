from django.http import Http404
from django.shortcuts import render

from app.models import User
from app.storage import load_objects


def _users() -> list[User]:
    return load_objects("users.json", User)


def user_list(request):
    """Show users without exposing their stored passwords."""
    return render(
        request,
        "users/user_list.html",
        {"users": _users()},
    )


def user_detail(request, user_id: int):
    """Show one user selected through a dynamic URL."""
    user = next(
        (item for item in _users() if item.id == user_id),
        None,
    )
    if user is None:
        raise Http404("Пользователь не найден")
    return render(
        request,
        "users/user_detail.html",
        {"user": user},
    )
