"""Загрузка и сохранение данных проекта в JSON-файлах."""
import json
from pathlib import Path

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


def load_books(path: Path = BOOKS_FILE) -> list[dict]:
    """Загрузить книги."""
    return load_json(path)


def save_books(books: list[dict], path: Path = BOOKS_FILE) -> None:
    """Сохранить книги."""
    save_json(path, books)


def load_readers(path: Path = READERS_FILE) -> list[dict]:
    """Загрузить читателей."""
    return load_json(path)


def save_readers(readers: list[dict], path: Path = READERS_FILE) -> None:
    """Сохранить читателей."""
    save_json(path, readers)


def load_loans(path: Path = LOANS_FILE) -> list[dict]:
    """Загрузить выдачи."""
    return load_json(path)


def save_loans(loans: list[dict], path: Path = LOANS_FILE) -> None:
    """Сохранить выдачи."""
    save_json(path, loans)
