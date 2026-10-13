"""Libris: консольное приложение учёта выдачи книг (ПР3, ООП)."""
from datetime import date

import storage
from models import Book, Loan, Reader
from models import books as books_mod
from models import loans as loans_mod
from models import readers as readers_mod
from utils import input_date, input_int, input_text

MENU = """
=== Libris: учёт выдачи книг ===
1. Показать книги
2. Найти книгу по названию
3. Книги автора
4. Проверить наличие книги
5. Выдать книгу
6. Принять книгу
7. Показать выдачи
8. Добавить книгу
9. Зарегистрировать читателя
0. Выход
"""


def show_books(books: list[Book]) -> None:
    """Вывести каталог, отсортированный по названию."""
    if not books:
        print("Каталог пуст.")
    for book in books_mod.sort_books(books):
        print(book)


def search_by_title(books: list[Book]) -> None:
    """Поиск книги по названию."""
    found = books_mod.find_books_by_title(books, input_text("Название: "))
    if not found:
        print("Ничего не найдено.")
    for book in found:
        print(book)


def search_by_author(books: list[Book]) -> None:
    """Отбор книг по автору."""
    found = books_mod.filter_books_by_author(books, input_text("Автор: "))
    if not found:
        print("Ничего не найдено.")
    for book in found:
        print(book)


def check_availability(books: list[Book], loans: list[Loan]) -> None:
    """Проверка наличия свободных экземпляров."""
    book_id = input_int("Номер книги: ")
    try:
        free = loans_mod.count_available(books, loans, book_id)
    except loans_mod.LibraryError as error:
        print(f"Ошибка: {error}")
        return
    print(f"Свободных экземпляров: {free}")


def issue_book(books: list[Book], readers: list[Reader],
               loans: list[Loan]) -> None:
    """Оформление выдачи."""
    book_id = input_int("Номер книги: ")
    reader_id = input_int("Номер читателя: ")
    issued = input_date("Дата выдачи (ГГГГ-ММ-ДД): ")
    try:
        loan = loans_mod.create_loan(
            books, readers, loans, book_id, reader_id, issued)
    except loans_mod.LibraryError as error:
        print(f"Ошибка: {error}")
        return
    storage.save_loans(loans)
    print(f"Выдача оформлена, вернуть до {loan.due_date}")


def accept_book(loans: list[Loan]) -> None:
    """Приём книги."""
    loan_id = input_int("Номер выдачи: ")
    returned = input_date("Дата возврата (ГГГГ-ММ-ДД): ")
    try:
        fine = loans_mod.return_book(loans, loan_id, returned)
    except loans_mod.LibraryError as error:
        print(f"Ошибка: {error}")
        return
    storage.save_loans(loans)
    print(f"Книга принята. Штраф: {fine:.2f} руб.")


def show_loans(loans: list[Loan]) -> None:
    """Вывод всех выдач."""
    if not loans:
        print("Выдач нет.")
    for loan in loans:
        print(loan)
    overdue = loans_mod.overdue_loans(loans, date.today())
    print(f"Просроченных выдач: {len(overdue)}")


def add_book(books: list[Book]) -> None:
    """Добавление книги в каталог."""
    title = input_text("Название: ")
    author = input_text("Автор: ")
    year = input_int("Год издания: ")
    copies = input_int("Число экземпляров: ")
    try:
        book = books_mod.add_book(books, title, author, year, copies)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    storage.save_books(books)
    print(f"Добавлено: {book}")


def add_reader(readers: list[Reader]) -> None:
    """Регистрация читателя."""
    name = input_text("ФИО: ")
    email = input_text("Email: ")
    try:
        reader = readers_mod.add_reader(readers, name, email)
    except ValueError as error:
        print(f"Ошибка: {error}")
        return
    storage.save_readers(readers)
    print(f"Читатель зарегистрирован: {reader}")


def main() -> None:
    """Главный цикл программы."""
    try:
        books = storage.load_books()
        readers = storage.load_readers()
        loans = storage.load_loans(books, readers)
    except storage.StorageError as error:
        print(f"Ошибка загрузки данных: {error}")
        return

    while True:
        print(MENU)
        choice = input("Выберите пункт: ").strip()
        if choice == "1":
            show_books(books)
        elif choice == "2":
            search_by_title(books)
        elif choice == "3":
            search_by_author(books)
        elif choice == "4":
            check_availability(books, loans)
        elif choice == "5":
            issue_book(books, readers, loans)
        elif choice == "6":
            accept_book(loans)
        elif choice == "7":
            show_loans(loans)
        elif choice == "8":
            add_book(books)
        elif choice == "9":
            add_reader(readers)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
