from django.urls import include, path


urlpatterns = [
    path("", include("homepage.urls")),
    path("mentors/", include("mentors_site.urls")),
    path("applications/", include("applications_site.urls")),
    path(
        "specializations/",
        include("specializations_site.urls"),
    ),
    path("users/", include("users_site.urls")),
]

handler404 = "homepage.views.page_not_found"
