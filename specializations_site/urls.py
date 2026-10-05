from django.urls import path

from . import views


app_name = "specializations"

urlpatterns = [
    path("", views.specialization_list, name="list"),
    path(
        "<int:specialization_id>/",
        views.specialization_detail,
        name="detail",
    ),
]
