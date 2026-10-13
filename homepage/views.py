from django.http import HttpResponse


def page(title, content):
    """Собрать HTML-страницу с общим каркасом и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/books/">Книги</a>
        <a class="nav-link" href="/loans/">Выдачи</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    content = """
    <h1 class="display-4">Libris</h1>
    <p class="lead">Система учёта выдачи книг в библиотеке.</p>
    <p>Основные разделы:</p>
    <a href="/books/" class="btn btn-primary me-2">Книги</a>
    <a href="/loans/" class="btn btn-secondary">Выдачи</a>
    """
    return HttpResponse(page("Libris", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
