"""Функции работы с читателями."""
from books import next_id


def add_reader(readers: list[dict], name: str, email: str) -> dict:
    """Зарегистрировать читателя и выдать номер билета."""
    if "@" not in email:
        raise ValueError("Некорректный адрес электронной почты")
    reader_id = next_id(readers)
    reader = {
        "id": reader_id,
        "name": name,
        "email": email,
        "card_number": f"LB-{reader_id:04d}",
    }
    readers.append(reader)
    return reader


def find_reader_by_id(readers: list[dict], reader_id: int) -> dict | None:
    """Найти читателя по идентификатору."""
    for reader in readers:
        if reader["id"] == reader_id:
            return reader
    return None


def format_reader(reader: dict) -> str:
    """Строка для вывода читателя."""
    return (
        f"[{reader['id']}] {reader['name']} "
        f"({reader['card_number']}, {reader['email']})"
    )
