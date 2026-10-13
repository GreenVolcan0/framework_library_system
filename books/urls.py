from django.urls import path

from books import views

app_name = "books"

urlpatterns = [
    path("", views.book_list, name="list"),
    path("<int:book_id>/", views.book_detail, name="detail"),
]
