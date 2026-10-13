from datetime import date

from django.http import Http404
from django.shortcuts import render

import storage
from models.loans import count_available


def book_list(request):
    books, _, loans = storage.load_library()
    for book in books:
        book.available = count_available(books, loans, book.id)
    return render(request, "books/book_list.html", {"books": books})


def book_detail(request, book_id):
    books, _, loans = storage.load_library()
    book = next((item for item in books if item.id == book_id), None)
    if book is None:
        raise Http404("Книга не найдена")
    book.available = count_available(books, loans, book_id)
    book_loans = [loan for loan in loans if loan.book.id == book_id]
    today = date.today()
    for loan in book_loans:
        loan.status = loan.get_status(today)
    context = {"book": book, "loans": book_loans}
    return render(request, "books/book_detail.html", context)
