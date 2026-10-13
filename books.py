"""Функции работы с книгами (коллекция словарей)."""


def next_id(items: list[dict]) -> int:
    """Вернуть следующий свободный идентификатор."""
    return max((item["id"] for item in items), default=0) + 1


def add_book(
    books: list[dict],
    title: str,
    author: str,
    year: int,
    copies: int,
) -> dict:
    """Добавить книгу в каталог и вернуть созданную запись."""
    if copies < 1:
        raise ValueError("Число экземпляров должно быть не меньше 1")
    book = {
        "id": next_id(books),
        "title": title,
        "author": author,
        "year": year,
        "copies": copies,
    }
    books.append(book)
    return book


def find_book_by_id(books: list[dict], book_id: int) -> dict | None:
    """Найти книгу по идентификатору."""
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def find_books_by_title(books: list[dict], query: str) -> list[dict]:
    """Найти книги, в названии которых есть подстрока (без регистра)."""
    query = query.lower()
    return [book for book in books if query in book["title"].lower()]


def filter_books_by_author(books: list[dict], author: str) -> list[dict]:
    """Отобрать книги автора."""
    author = author.lower()
    return [book for book in books if author in book["author"].lower()]


def sort_books(
    books: list[dict],
    key: str = "title",
    reverse: bool = False,
) -> list[dict]:
    """Вернуть книги, отсортированные по полю key."""
    return sorted(books, key=lambda book: book[key], reverse=reverse)


def format_book(book: dict) -> str:
    """Строка для вывода книги."""
    return (
        f"[{book['id']}] {book['title']} — {book['author']}, "
        f"{book['year']} г., экземпляров: {book['copies']}"
    )
