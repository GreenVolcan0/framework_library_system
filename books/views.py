from django.http import Http404, HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page
from models.loans import count_available


def book_list(request):
    books, _, _ = storage.load_library()
    rows = "".join(
        f'<li class="list-group-item">'
        f'<a href="/books/{book.id}/">{escape(book.title)}</a> — '
        f"{escape(book.author)}, {book.year}</li>"
        for book in books
    )
    content = f"""
    <h1>Книги</h1>
    <ul class="list-group">{rows}</ul>
    """
    return HttpResponse(page("Книги", content))


def book_detail(request, book_id):
    books, _, loans = storage.load_library()
    book = next((item for item in books if item.id == book_id), None)
    if book is None:
        raise Http404("Книга не найдена")
    free = count_available(books, loans, book_id)
    content = f"""
    <h1>{escape(book.title)}</h1>
    <p class="lead">{escape(book.author)}, {book.year} г.</p>
    <p>Всего экземпляров: {book.copies}. Свободно: {free}.</p>
    <a href="/books/" class="btn btn-secondary">К списку книг</a>
    """
    return HttpResponse(page(book.title, content))
