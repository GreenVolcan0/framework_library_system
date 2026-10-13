import pytest

from models.books import (Book, add_book, filter_books_by_author,
                          find_books_by_title, sort_books)


@pytest.fixture
def catalog():
    books = []
    add_book(books, "Война и мир", "Л. Н. Толстой", 1869, 2)
    add_book(books, "Анна Каренина", "Л. Н. Толстой", 1877, 1)
    add_book(books, "Евгений Онегин", "А. С. Пушкин", 1833, 2)
    return books


def test_add_book_creates_object_with_sequential_id(catalog):
    book = add_book(catalog, "Чистый код", "Р. Мартин", 2008, 1)
    assert isinstance(book, Book)
    assert book.id == 4
    assert len(catalog) == 4


def test_book_rejects_zero_copies():
    with pytest.raises(ValueError):
        Book(1, "Книга", "Автор", 2000, 0)


def test_book_copies_setter_validates():
    book = Book(1, "Книга", "Автор", 2000, 2)
    with pytest.raises(ValueError):
        book.copies = -1
    assert book.copies == 2


def test_book_str():
    book = Book(1, "Война и мир", "Л. Н. Толстой", 1869, 2)
    assert str(book) == (
        "[1] Война и мир — Л. Н. Толстой, 1869 г., экземпляров: 2")


def test_book_dict_roundtrip():
    book = Book(7, "Книга", "Автор", 2001, 3)
    assert Book.from_dict(book.to_dict()).to_dict() == book.to_dict()


def test_find_books_by_title_is_case_insensitive(catalog):
    found = find_books_by_title(catalog, "ВОЙНА")
    assert [book.title for book in found] == ["Война и мир"]


def test_filter_books_by_author(catalog):
    assert len(filter_books_by_author(catalog, "толстой")) == 2


def test_sort_books_by_year_descending(catalog):
    years = [b.year for b in sort_books(catalog, "year", reverse=True)]
    assert years == [1877, 1869, 1833]
