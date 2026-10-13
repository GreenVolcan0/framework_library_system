from datetime import date

import pytest

from books import add_book
from loans import (LibraryError, calculate_due_date, calculate_fine,
                   count_available, create_loan, overdue_loans, return_book)
from readers import add_reader
from storage import StorageError, load_json, save_json


@pytest.fixture
def library():
    books, readers, loans = [], [], []
    add_book(books, "Война и мир", "Л. Н. Толстой", 1869, 1)
    add_reader(readers, "Иванов Пётр", "ivanov@example.com")
    return books, readers, loans


def test_due_date_is_14_days_after_issue():
    assert calculate_due_date(date(2026, 9, 15)) == date(2026, 9, 29)


def test_fine_zero_when_returned_in_time():
    assert calculate_fine(date(2026, 9, 29), date(2026, 9, 29)) == 0.0


def test_fine_for_overdue_days():
    assert calculate_fine(date(2026, 9, 29), date(2026, 10, 3)) == 20.0


def test_create_loan_reduces_available_copies(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 10, 1))
    assert count_available(books, loans, 1) == 0


def test_cannot_issue_when_no_copies_left(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 10, 1))
    with pytest.raises(LibraryError):
        create_loan(books, readers, loans, 1, 1, date(2026, 10, 2))


def test_return_book_returns_fine_and_frees_copy(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    fine = return_book(loans, 1, date(2026, 10, 3))
    assert fine == 20.0
    assert count_available(books, loans, 1) == 1


def test_overdue_loans(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 9, 1))
    assert len(overdue_loans(loans, date(2026, 10, 1))) == 1


def test_json_roundtrip(tmp_path):
    path = tmp_path / "items.json"
    save_json(path, [{"id": 1, "title": "Книга"}])
    assert load_json(path) == [{"id": 1, "title": "Книга"}]


def test_broken_json_raises_storage_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{не json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_json(path)
