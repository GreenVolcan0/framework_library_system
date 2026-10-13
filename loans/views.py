from django.http import Http404, HttpResponse
from django.utils.html import escape

import storage
from homepage.views import page


def loan_list(request):
    _, _, loans = storage.load_library()
    rows = "".join(
        f"<tr><td><a href=\"/loans/{loan.id}/\">{loan.id}</a></td>"
        f"<td>{escape(loan.book.title)}</td>"
        f"<td>{escape(loan.reader.name)}</td>"
        f"<td>{loan.due_date}</td></tr>"
        for loan in loans
    )
    content = f"""
    <h1>Выдачи</h1>
    <table class="table">
        <thead><tr><th>№</th><th>Книга</th><th>Читатель</th>
        <th>Вернуть до</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """
    return HttpResponse(page("Выдачи", content))


def loan_detail(request, loan_id):
    _, _, loans = storage.load_library()
    loan = next((item for item in loans if item.id == loan_id), None)
    if loan is None:
        raise Http404("Выдача не найдена")
    returned = loan.return_date or "не возвращена"
    content = f"""
    <h1>Выдача № {loan.id}</h1>
    <p>Книга: <a href="/books/{loan.book.id}/">
        {escape(loan.book.title)}</a></p>
    <p>Читатель: {escape(loan.reader.name)}</p>
    <p>Выдана: {loan.issue_date}. Вернуть до: {loan.due_date}.</p>
    <p>Возврат: {returned}</p>
    <a href="/loans/" class="btn btn-secondary">К списку выдач</a>
    """
    return HttpResponse(page(f"Выдача {loan.id}", content))
