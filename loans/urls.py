from django.urls import path

from loans import views

app_name = "loans"

urlpatterns = [
    path("", views.loan_list, name="list"),
    path("<int:loan_id>/", views.loan_detail, name="detail"),
]
