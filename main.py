"""Libris: начальный сценарий (ПР1) — выдача книги читателю."""
from datetime import date, timedelta

LOAN_DAYS = 14
FINE_PER_DAY = 5.0

book_title = "Мастер и Маргарита"
book_author = "М. А. Булгаков"
copies_total = 3
copies_on_loan = 3 - 1
reader_name = "Беляева Анна"
issue_date = date(2026, 9, 15)
return_date = date(2026, 10, 3)


def get_book_status(total: int, on_loan: int) -> str:
    """Вернуть статус книги по числу экземпляров."""
    available = total - on_loan
    if available > 1:
        return f"Книга доступна, свободных экземпляров: {available}"
    if available == 1:
        return "Остался последний экземпляр"
    return "Все экземпляры выданы"


def calculate_due_date(issued: date, days: int = LOAN_DAYS) -> date:
    """Рассчитать срок возврата книги."""
    return issued + timedelta(days=days)


def calculate_fine(due: date, returned: date) -> float:
    """Рассчитать штраф за просрочку возврата."""
    if returned <= due:
        return 0.0
    return (returned - due).days * FINE_PER_DAY


due_date = calculate_due_date(issue_date)
fine = calculate_fine(due_date, return_date)

print(f"Книга: {book_title} ({book_author})")
print(get_book_status(copies_total, copies_on_loan))
print(f"Читатель: {reader_name}")
print(f"Дата выдачи: {issue_date}")
print(f"Вернуть до: {due_date}")
if fine > 0:
    print(f"Книга возвращена {return_date}, штраф: {fine:.2f} руб.")
else:
    print("Книга возвращена вовремя, штрафа нет")
