from datetime import date

import pytest

from models.books import add_book
from models.loans import (LibraryError, Loan, count_available, create_loan,
                          overdue_loans, return_book)
from models.readers import add_reader
from storage import (StorageError, load_books, load_json, load_loans,
                     load_readers, save_books, save_json, save_loans,
                     save_readers)


@pytest.fixture
def library():
    books, readers, loans = [], [], []
    add_book(books, "Война и мир", "Л. Н. Толстой", 1869, 1)
    add_reader(readers, "Иванов Пётр", "ivanov@example.com")
    return books, readers, loans


def test_due_date_is_14_days_after_issue(library):
    books, readers, loans = library
    loan = create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    assert loan.due_date == date(2026, 9, 29)


def test_loan_links_objects(library):
    books, readers, loans = library
    loan = create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    assert loan.book is books[0]
    assert loan.reader is readers[0]
    assert "Война и мир" in str(loan)


def test_fine_zero_when_returned_in_time(library):
    books, readers, loans = library
    loan = create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    assert loan.calculate_fine(date(2026, 9, 29)) == 0.0


def test_fine_for_overdue_days(library):
    books, readers, loans = library
    loan = create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    assert loan.calculate_fine(date(2026, 10, 3)) == 20.0


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


def test_cannot_return_twice(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    return_book(loans, 1, date(2026, 9, 20))
    with pytest.raises(LibraryError):
        return_book(loans, 1, date(2026, 9, 21))


def test_overdue_loans(library):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 9, 1))
    assert len(overdue_loans(loans, date(2026, 10, 1))) == 1


def test_objects_roundtrip_through_json(library, tmp_path):
    books, readers, loans = library
    create_loan(books, readers, loans, 1, 1, date(2026, 9, 15))
    save_books(books, tmp_path / "b.json")
    save_readers(readers, tmp_path / "r.json")
    save_loans(loans, tmp_path / "l.json")
    new_books = load_books(tmp_path / "b.json")
    new_readers = load_readers(tmp_path / "r.json")
    new_loans = load_loans(new_books, new_readers, tmp_path / "l.json")
    assert isinstance(new_loans[0], Loan)
    assert new_loans[0].book.title == "Война и мир"
    assert new_loans[0].due_date == date(2026, 9, 29)


def test_json_roundtrip(tmp_path):
    path = tmp_path / "items.json"
    save_json(path, [{"id": 1, "title": "Книга"}])
    assert load_json(path) == [{"id": 1, "title": "Книга"}]


def test_broken_json_raises_storage_error(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{не json", encoding="utf-8")
    with pytest.raises(StorageError):
        load_json(path)
