"""Книга и функции работы с каталогом."""


class Book:
    """Книга библиотечного фонда."""

    def __init__(self, book_id: int, title: str, author: str,
                 year: int, copies: int) -> None:
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    @property
    def copies(self) -> int:
        """Общее число экземпляров книги."""
        return self._copies

    @copies.setter
    def copies(self, value: int) -> None:
        if value < 1:
            raise ValueError("Число экземпляров должно быть не меньше 1")
        self._copies = value

    def matches_title(self, query: str) -> bool:
        """Содержится ли подстрока в названии (без учёта регистра)."""
        return query.lower() in self.title.lower()

    def is_by_author(self, author: str) -> bool:
        """Написана ли книга указанным автором."""
        return author.lower() in self.author.lower()

    def to_dict(self) -> dict:
        """Представление для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "copies": self.copies,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Создать книгу из словаря JSON."""
        return cls(data["id"], data["title"], data["author"],
                   data["year"], data["copies"])

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.title} — {self.author}, "
            f"{self.year} г., экземпляров: {self.copies}"
        )


def next_book_id(books: list[Book]) -> int:
    """Следующий свободный идентификатор книги."""
    return max((book.id for book in books), default=0) + 1


def add_book(books: list[Book], title: str, author: str,
             year: int, copies: int) -> Book:
    """Создать книгу и добавить её в каталог."""
    book = Book(next_book_id(books), title, author, year, copies)
    books.append(book)
    return book


def find_book_by_id(books: list[Book], book_id: int) -> Book | None:
    """Найти книгу по идентификатору."""
    for book in books:
        if book.id == book_id:
            return book
    return None


def find_books_by_title(books: list[Book], query: str) -> list[Book]:
    """Найти книги по части названия."""
    return [book for book in books if book.matches_title(query)]


def filter_books_by_author(books: list[Book], author: str) -> list[Book]:
    """Отобрать книги автора."""
    return [book for book in books if book.is_by_author(author)]


def sort_books(books: list[Book], key: str = "title",
               reverse: bool = False) -> list[Book]:
    """Отсортировать книги по атрибуту key."""
    return sorted(books, key=lambda book: getattr(book, key),
                  reverse=reverse)
