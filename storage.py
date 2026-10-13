"""Загрузка и сохранение данных проекта в JSON-файлах."""
import json
from pathlib import Path

from models import Book, Loan, Reader
from models.loans import LibraryError

DATA_DIR = Path(__file__).resolve().parent / "data"
BOOKS_FILE = DATA_DIR / "books.json"
READERS_FILE = DATA_DIR / "readers.json"
LOANS_FILE = DATA_DIR / "loans.json"


class StorageError(Exception):
    """Ошибка чтения или записи файла данных."""


def load_json(path: Path) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет, возвращается пустой список. Повреждённый файл
    приводит к StorageError.
    """
    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise StorageError(f"Файл {path.name} повреждён: {error}")


def save_json(path: Path, items: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise StorageError(f"Не удалось записать {path.name}: {error}")


def load_books(path: Path = BOOKS_FILE) -> list[Book]:
    """Загрузить книги как объекты Book."""
    return [Book.from_dict(item) for item in load_json(path)]


def save_books(books: list[Book], path: Path = BOOKS_FILE) -> None:
    """Сохранить книги."""
    save_json(path, [book.to_dict() for book in books])


def load_readers(path: Path = READERS_FILE) -> list[Reader]:
    """Загрузить читателей как объекты Reader."""
    return [Reader.from_dict(item) for item in load_json(path)]


def save_readers(readers: list[Reader], path: Path = READERS_FILE) -> None:
    """Сохранить читателей."""
    save_json(path, [reader.to_dict() for reader in readers])


def load_loans(books: list[Book], readers: list[Reader],
               path: Path = LOANS_FILE) -> list[Loan]:
    """Загрузить выдачи, восстановив связи с книгами и читателями."""
    try:
        return [Loan.from_dict(item, books, readers)
                for item in load_json(path)]
    except LibraryError as error:
        raise StorageError(str(error))


def save_loans(loans: list[Loan], path: Path = LOANS_FILE) -> None:
    """Сохранить выдачи."""
    save_json(path, [loan.to_dict() for loan in loans])
