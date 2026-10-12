from django.http import Http404
from django.shortcuts import render

from app.models import Specialization
from app.storage import load_objects


def _specializations() -> list[Specialization]:
    return load_objects("specializations.json", Specialization)


def specialization_list(request):
    """Show all available learning directions."""
    return render(
        request,
        "specializations/specialization_list.html",
        {"specializations": _specializations()},
    )


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
    return render(
        request,
        "specializations/specialization_detail.html",
        {"specialization": item},
    )
