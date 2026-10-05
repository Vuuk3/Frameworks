from django.urls import path

from . import views


app_name = "mentors"

urlpatterns = [
    path("", views.mentor_list, name="list"),
    path("<int:mentor_id>/", views.mentor_detail, name="detail"),
]
