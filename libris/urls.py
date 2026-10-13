"""Корневая маршрутизация проекта Libris."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("books/", include("books.urls")),
    path("loans/", include("loans.urls")),
]

handler404 = "homepage.views.page_not_found"
