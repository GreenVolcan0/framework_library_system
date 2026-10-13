from django.shortcuts import render

import storage
from models.loans import active_loans


def index(request):
    books, _, loans = storage.load_library()
    context = {
        "books_count": len(books),
        "active_count": len(active_loans(loans)),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
