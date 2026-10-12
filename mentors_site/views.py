from django.http import Http404
from django.shortcuts import render

from app.models import Mentor, Specialization
from app.storage import load_objects


def _mentors() -> list[Mentor]:
    return load_objects("mentors.json", Mentor)


def _specialization_names() -> dict[int, str]:
    items = load_objects("specializations.json", Specialization)
    return {item.id: item.name for item in items}


def mentor_list(request):
    """Show all mentors stored by the console application."""
    names = _specialization_names()
    mentors = []
    for mentor in _mentors():
        mentor.specialization_names = [
            names.get(item, f"№{item}")
            for item in mentor.specializations
        ]
        mentors.append(mentor)
    return render(
        request,
        "mentors/mentor_list.html",
        {"mentors": mentors},
    )


def mentor_detail(request, mentor_id: int):
    """Show one mentor selected through a dynamic URL."""
    mentor = next(
        (item for item in _mentors() if item.id == mentor_id),
        None,
    )
    if mentor is None:
        raise Http404("Наставник не найден")

    names = _specialization_names()
    specialization_names = [
        names.get(item, f"№{item}")
        for item in mentor.specializations
    ]
    return render(
        request,
        "mentors/mentor_detail.html",
        {
            "mentor": mentor,
            "specialization_names": specialization_names,
        },
    )
