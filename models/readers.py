"""Читатель библиотеки."""
from models.users import User


class Reader(User):
    """Читатель — пользователь с читательским билетом."""

    def __init__(self, reader_id: int, name: str, email: str,
                 card_number: str | None = None) -> None:
        super().__init__(reader_id, name, email)
        self.card_number = card_number or f"LB-{reader_id:04d}"

    def to_dict(self) -> dict:
        """Представление для сохранения в JSON."""
        data = super().to_dict()
        data["card_number"] = self.card_number
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Reader":
        """Создать читателя из словаря JSON."""
        return cls(data["id"], data["name"], data["email"],
                   data.get("card_number"))

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.card_number}, {self.email})"


def next_reader_id(readers: list[Reader]) -> int:
    """Следующий свободный идентификатор читателя."""
    return max((reader.id for reader in readers), default=0) + 1


def add_reader(readers: list[Reader], name: str, email: str) -> Reader:
    """Зарегистрировать читателя и добавить в коллекцию."""
    reader = Reader(next_reader_id(readers), name, email)
    readers.append(reader)
    return reader


def find_reader_by_id(readers: list[Reader],
                      reader_id: int) -> Reader | None:
    """Найти читателя по идентификатору."""
    for reader in readers:
        if reader.id == reader_id:
            return reader
    return None
