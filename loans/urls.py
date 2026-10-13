from django.urls import path

from loans import views

urlpatterns = [
    path("", views.loan_list, name="loan_list"),
    path("<int:loan_id>/", views.loan_detail, name="loan_detail"),
]
