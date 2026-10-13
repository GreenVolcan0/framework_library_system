from datetime import date

from django.http import Http404
from django.shortcuts import render

import storage


def loan_list(request):
    _, _, loans = storage.load_library()
    today = date.today()
    for loan in loans:
        loan.status = loan.get_status(today)
    return render(request, "loans/loan_list.html", {"loans": loans})


def loan_detail(request, loan_id):
    _, _, loans = storage.load_library()
    loan = next((item for item in loans if item.id == loan_id), None)
    if loan is None:
        raise Http404("Выдача не найдена")
    today = date.today()
    loan.status = loan.get_status(today)
    context = {"loan": loan}
    if loan.status == "overdue":
        context["overdue_days"] = (today - loan.due_date).days
        context["fine"] = loan.calculate_fine(today)
    return render(request, "loans/loan_detail.html", context)
