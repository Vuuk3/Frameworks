from django.http import Http404
from django.shortcuts import render

from app.models import Application, Mentor, Specialization, User
from app.storage import load_objects


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
    applications = []
    for item in _applications():
        user = users.get(item.user_id)
        specialization = specializations.get(item.specialization_id)
        item.user_name = (
            user.name
            if user
            else f"Пользователь №{item.user_id}"
        )
        item.specialization_name = (
            specialization.name
            if specialization
            else f"Специализация №{item.specialization_id}"
        )
        applications.append(item)
    return render(
        request,
        "applications/application_list.html",
        {"applications": applications},
    )


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
    return render(
        request,
        "applications/application_detail.html",
        {
            "application": application,
            "user": user,
            "mentor": mentor,
            "specialization_name": specialization_name,
        },
    )
