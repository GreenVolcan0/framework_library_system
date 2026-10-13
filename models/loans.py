"""Выдача книги читателю и операции над выдачами."""
from datetime import date, timedelta

from models.books import Book, find_book_by_id
from models.readers import Reader, find_reader_by_id
from utils import FINE_PER_DAY, LOAN_DAYS


class LibraryError(Exception):
    """Нарушение правил работы библиотеки."""


class Loan:
    """Выдача: связывает объект Book с объектом Reader."""

    def __init__(self, loan_id: int, book: Book, reader: Reader,
                 issue_date: date, due_date: date | None = None,
                 return_date: date | None = None) -> None:
        self.id = loan_id
        self.book = book
        self.reader = reader
        self.issue_date = issue_date
        self.due_date = due_date or issue_date + timedelta(days=LOAN_DAYS)
        self.return_date = return_date

    @property
    def is_active(self) -> bool:
        """Книга ещё не возвращена."""
        return self.return_date is None

    def is_overdue(self, today: date) -> bool:
        """Просрочена ли невозвращённая выдача."""
        return self.is_active and self.due_date < today

    def get_status(self, today: date) -> str:
        """Статус выдачи: returned, overdue или active."""
        if not self.is_active:
            return "returned"
        return "overdue" if self.is_overdue(today) else "active"

    def calculate_fine(self, returned: date) -> float:
        """Штраф при возврате в указанную дату."""
        if returned <= self.due_date:
            return 0.0
        return (returned - self.due_date).days * FINE_PER_DAY

    def close(self, returned: date) -> float:
        """Принять книгу и вернуть сумму штрафа."""
        if not self.is_active:
            raise LibraryError("Книга уже возвращена")
        self.return_date = returned
        return self.calculate_fine(returned)

    def to_dict(self) -> dict:
        """Представление для сохранения в JSON (ссылки по id)."""
        return {
            "id": self.id,
            "book_id": self.book.id,
            "reader_id": self.reader.id,
            "issue_date": self.issue_date.isoformat(),
            "due_date": self.due_date.isoformat(),
            "return_date": (self.return_date.isoformat()
                            if self.return_date else None),
        }

    @classmethod
    def from_dict(cls, data: dict, books: list[Book],
                  readers: list[Reader]) -> "Loan":
        """Создать выдачу из словаря, восстановив связи с объектами."""
        book = find_book_by_id(books, data["book_id"])
        reader = find_reader_by_id(readers, data["reader_id"])
        if book is None or reader is None:
            raise LibraryError(
                f"Выдача {data['id']} ссылается на несуществующие данные")
        returned = data["return_date"]
        return cls(
            data["id"], book, reader,
            date.fromisoformat(data["issue_date"]),
            date.fromisoformat(data["due_date"]),
            date.fromisoformat(returned) if returned else None,
        )

    def __str__(self) -> str:
        status = self.return_date or "не возвращена"
        return (
            f"[{self.id}] «{self.book.title}» — {self.reader.name}, "
            f"выдана {self.issue_date}, вернуть до {self.due_date}, "
            f"возврат: {status}"
        )


def active_loans(loans: list[Loan]) -> list[Loan]:
    """Выдачи, по которым книга не возвращена."""
    return [loan for loan in loans if loan.is_active]


def count_available(books: list[Book], loans: list[Loan],
                    book_id: int) -> int:
    """Число свободных экземпляров книги."""
    book = find_book_by_id(books, book_id)
    if book is None:
        raise LibraryError(f"Книга {book_id} не найдена")
    on_loan = sum(1 for loan in active_loans(loans)
                  if loan.book.id == book_id)
    return book.copies - on_loan


def create_loan(books: list[Book], readers: list[Reader],
                loans: list[Loan], book_id: int, reader_id: int,
                issued: date) -> Loan:
    """Оформить выдачу книги читателю."""
    reader = find_reader_by_id(readers, reader_id)
    if reader is None:
        raise LibraryError(f"Читатель {reader_id} не найден")
    if count_available(books, loans, book_id) < 1:
        raise LibraryError("Все экземпляры книги выданы")
    book = find_book_by_id(books, book_id)
    loan_id = max((loan.id for loan in loans), default=0) + 1
    loan = Loan(loan_id, book, reader, issued)
    loans.append(loan)
    return loan


def find_loan_by_id(loans: list[Loan], loan_id: int) -> Loan | None:
    """Найти выдачу по идентификатору."""
    for loan in loans:
        if loan.id == loan_id:
            return loan
    return None


def return_book(loans: list[Loan], loan_id: int, returned: date) -> float:
    """Принять книгу по номеру выдачи и вернуть штраф."""
    loan = find_loan_by_id(loans, loan_id)
    if loan is None:
        raise LibraryError(f"Выдача {loan_id} не найдена")
    return loan.close(returned)


def overdue_loans(loans: list[Loan], today: date) -> list[Loan]:
    """Просроченные невозвращённые выдачи."""
    return [loan for loan in loans if loan.is_overdue(today)]
