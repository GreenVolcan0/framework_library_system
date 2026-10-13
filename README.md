# Libris

## Назначение

Libris — приложение для учёта выдачи книг в библиотеке. Оно позволяет
узнать, доступна ли книга, оформить выдачу читателю, рассчитать срок
возврата и штраф за просрочку.

## Целевая аудитория

- сотрудники небольших библиотек (школьных, вузовских, районных),
  которые ведут учёт книг и выдач;
- читатели, которым нужно узнать, есть ли книга в наличии и когда
  её нужно вернуть.

## Предметная область

Библиотечный учёт: в фонде библиотеки хранятся книги в нескольких
экземплярах, читатели получают книги на ограниченный срок, а за
просрочку возврата начисляется штраф.

## Основные сущности

- Книга (Book) — название, автор, год издания, число экземпляров;
- Читатель (Reader) — ФИО, электронная почта, номер читательского билета;
- Выдача (Loan) — книга, читатель, дата выдачи, срок возврата, статус.

## Основные функции

- проверка наличия книги и вывод статуса («доступна» / «выдана»);
- расчёт срока возврата книги по дате выдачи;
- расчёт штрафа за просрочку возврата.

## Возможности (ПР2)

Консольное меню:

1. показать каталог (сортировка по названию);
2. найти книгу по названию;
3. отобрать книги автора;
4. проверить наличие свободных экземпляров;
5. выдать книгу читателю;
6. принять книгу (с расчётом штрафа);
7. показать выдачи и число просроченных;
8. добавить книгу;
9. зарегистрировать читателя.

Некорректный ввод (буква вместо числа, неверная дата, несуществующий
номер) обрабатывается и не приводит к аварийному завершению.

## Структура проекта

```
library_system/
├── README.md
├── main.py        # консольное меню
├── storage.py     # загрузка и сохранение объектов в JSON
├── utils.py       # ввод данных, константы
├── models/
│   ├── users.py   # класс User
│   ├── readers.py # класс Reader(User) и функции коллекции читателей
│   ├── books.py   # класс Book и функции каталога
│   └── loans.py   # класс Loan и функции выдачи/возврата
├── data/          # books.json, readers.json, loans.json
└── tests/         # тесты pytest
```

## Объектная модель (ПР3)

| Класс | Атрибуты | Методы |
|-------|----------|--------|
| `User` | `id`, `name`, `email` | `to_dict()`, `__str__()` |
| `Reader(User)` | + `card_number` | `from_dict()`, `to_dict()`, `__str__()` |
| `Book` | `id`, `title`, `author`, `year`, `copies` | `matches_title()`, `is_by_author()`, `to_dict()`, `from_dict()`, `__str__()` |
| `Loan` | `id`, `book`, `reader`, `issue_date`, `due_date`, `return_date` | `is_active`, `is_overdue()`, `calculate_fine()`, `close()`, `to_dict()`, `from_dict()`, `__str__()` |

- **Взаимодействие объектов (композиция):** `Loan` хранит ссылки на объекты
  `Book` и `Reader`, а не их идентификаторы; в JSON сохраняются только
  `book_id` и `reader_id`, а при загрузке связи восстанавливаются.
- **Инкапсуляция:** число экземпляров `Book.copies` и адрес
  `User.email` проверяются в свойствах (`property`) при каждом изменении.
- **Наследование:** `Reader` является `User` с читательским билетом.
- **Полиморфизм:** `print(obj)` вызывает собственный `__str__()` у
  каждого класса.
- Функции обработки коллекций (`find_books_by_title()`,
  `count_available()`, `create_loan()` и др.) остались обычными функциями
  модулей `models/*.py`.

## Формат данных

Данные хранятся в JSON-файлах каталога `data/`. Каждый файл — список
словарей. Даты записываются строкой `ГГГГ-ММ-ДД`.

- `books.json`: `id`, `title`, `author`, `year`, `copies`;
- `readers.json`: `id`, `name`, `email`, `card_number`;
- `loans.json`: `id`, `book_id`, `reader_id`, `issue_date`,
  `due_date`, `return_date` (`null`, пока книга не возвращена).

## Веб-интерфейс (ПР5–ПР6)

Консольная версия сохранена; поверх тех же объектов и JSON-файлов
добавлено Django-приложение (Django 5.2). Данные загружаются функцией
`storage.load_library()`.

| URL | Имя маршрута | View | Шаблон |
|-----|--------------|------|--------|
| `/` | `homepage:index` | `homepage.views.index` | `homepage/index.html` |
| `/books/` | `books:list` | `books.views.book_list` | `books/book_list.html` |
| `/books/<id>/` | `books:detail` | `books.views.book_detail` | `books/book_detail.html` |
| `/loans/` | `loans:list` | `loans.views.loan_list` | `loans/loan_list.html` |
| `/loans/<id>/` | `loans:detail` | `loans.views.loan_detail` | `loans/loan_detail.html` |

Django-проект `libris`, приложения: `homepage`, `books`, `loans`.
Несуществующие адреса и объекты обрабатываются `handler404`
(`homepage.views.page_not_found`, шаблон `templates/404.html`).

### Шаблоны (ПР6)

HTML формируется только в шаблонах; view-функции готовят контекст и
вызывают `render()`. Функция `page()` из ПР5 удалена.

```
templates/
├── base.html                  # общий каркас: Bootstrap, CSS, логотип, JS
├── 404.html
└── includes/navigation.html   # навигация через {% url %}
homepage/templates/homepage/index.html
books/templates/books/{book_list,book_detail}.html
books/templates/books/includes/book_card.html
loans/templates/loans/{loan_list,loan_detail}.html
loans/templates/loans/includes/loan_status.html
```

Использовано: `{% extends %}` и `{% block %}`, `{% include %}`,
`{% for ... empty %}`, `{% if %}`, именованные URL с пространствами
имён, фильтры `length`, `default`, `date`, `truncatechars`,
`floatformat`.

### Статические файлы

`homepage/static/homepage/`: `css/style.css` (собственное оформление
карточек, статусов и навигации), `js/main.js` (текущий год в подвале),
`img/logo.png` (логотип).

## Запуск

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py             # консольная версия
python manage.py check     # проверка Django-проекта
python manage.py runserver # веб-версия: http://127.0.0.1:8000/
pytest -v                  # тесты
flake8                     # проверка оформления кода
```
