"""Вспомогательные функции: ввод данных и константы проекта."""
from datetime import date

LOAN_DAYS = 14
FINE_PER_DAY = 5.0


def input_int(prompt: str, min_value: int = 1) -> int:
    """Запрашивать целое число, пока не будет введено корректное."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("Ошибка: нужно ввести целое число.")
            continue
        if value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}.")
            continue
        return value


def input_date(prompt: str) -> date:
    """Запрашивать дату в формате ГГГГ-ММ-ДД."""
    while True:
        raw = input(prompt).strip()
        try:
            return date.fromisoformat(raw)
        except ValueError:
            print("Ошибка: дата должна быть в формате ГГГГ-ММ-ДД.")


def input_text(prompt: str) -> str:
    """Запрашивать непустую строку."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("Ошибка: значение не может быть пустым.")
