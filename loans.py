"""Функции работы с выдачами книг."""
from datetime import date, timedelta

from books import find_book_by_id, next_id
from readers import find_reader_by_id
from utils import FINE_PER_DAY, LOAN_DAYS


class LibraryError(Exception):
    """Нарушение правил работы библиотеки."""


def active_loans(loans: list[dict]) -> list[dict]:
    """Выдачи, по которым книга ещё не возвращена."""
    return [loan for loan in loans if loan["return_date"] is None]


def count_available(books: list[dict], loans: list[dict],
                    book_id: int) -> int:
    """Число свободных экземпляров книги."""
    book = find_book_by_id(books, book_id)
    if book is None:
        raise LibraryError(f"Книга {book_id} не найдена")
    on_loan = sum(1 for loan in active_loans(loans)
                  if loan["book_id"] == book_id)
    return book["copies"] - on_loan


def calculate_due_date(issued: date, days: int = LOAN_DAYS) -> date:
    """Срок возврата книги."""
    return issued + timedelta(days=days)


def calculate_fine(due: date, returned: date) -> float:
    """Штраф за просрочку возврата."""
    if returned <= due:
        return 0.0
    return (returned - due).days * FINE_PER_DAY


def create_loan(
    books: list[dict],
    readers: list[dict],
    loans: list[dict],
    book_id: int,
    reader_id: int,
    issued: date,
) -> dict:
    """Оформить выдачу книги читателю."""
    if find_reader_by_id(readers, reader_id) is None:
        raise LibraryError(f"Читатель {reader_id} не найден")
    if count_available(books, loans, book_id) < 1:
        raise LibraryError("Все экземпляры книги выданы")
    loan = {
        "id": next_id(loans),
        "book_id": book_id,
        "reader_id": reader_id,
        "issue_date": issued.isoformat(),
        "due_date": calculate_due_date(issued).isoformat(),
        "return_date": None,
    }
    loans.append(loan)
    return loan


def return_book(loans: list[dict], loan_id: int, returned: date) -> float:
    """Принять книгу и вернуть сумму штрафа."""
    for loan in loans:
        if loan["id"] == loan_id:
            if loan["return_date"] is not None:
                raise LibraryError("Книга уже возвращена")
            loan["return_date"] = returned.isoformat()
            due = date.fromisoformat(loan["due_date"])
            return calculate_fine(due, returned)
    raise LibraryError(f"Выдача {loan_id} не найдена")


def overdue_loans(loans: list[dict], today: date) -> list[dict]:
    """Просроченные невозвращённые выдачи."""
    return [
        loan for loan in active_loans(loans)
        if date.fromisoformat(loan["due_date"]) < today
    ]


def format_loan(loan: dict, books: list[dict],
                readers: list[dict]) -> str:
    """Строка для вывода выдачи."""
    book = find_book_by_id(books, loan["book_id"])
    reader = find_reader_by_id(readers, loan["reader_id"])
    title = book["title"] if book else "?"
    name = reader["name"] if reader else "?"
    status = loan["return_date"] or "не возвращена"
    return (
        f"[{loan['id']}] «{title}» — {name}, выдана {loan['issue_date']}, "
        f"вернуть до {loan['due_date']}, возврат: {status}"
    )
