"""Базовый класс пользователя системы."""


class User:
    """Пользователь библиотеки: имя и адрес электронной почты."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email

    @property
    def email(self) -> str:
        """Адрес электронной почты."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Некорректный адрес электронной почты")
        self._email = value

    def to_dict(self) -> dict:
        """Представление для сохранения в JSON."""
        return {"id": self.id, "name": self.name, "email": self.email}

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
