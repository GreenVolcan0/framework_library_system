from pathlib import Path

import pytest
from django.test import Client, override_settings
from django.urls import reverse

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def client():
    return Client()


@pytest.mark.parametrize("url", [
    "/", "/books/", "/books/1/", "/loans/", "/loans/1/",
])
def test_pages_open(client, url):
    assert client.get(url).status_code == 200


@pytest.mark.parametrize("url", [
    "/books/999/", "/loans/999/", "/books/abc/", "/nonexistent/",
])
def test_missing_pages_return_404(client, url):
    with override_settings(DEBUG=False):
        response = client.get(url)
    assert response.status_code == 404
    assert "404 – страница не найдена" in response.content.decode()


def test_named_urls_with_namespaces():
    assert reverse("homepage:index") == "/"
    assert reverse("books:list") == "/books/"
    assert reverse("books:detail", args=[3]) == "/books/3/"
    assert reverse("loans:list") == "/loans/"
    assert reverse("loans:detail", args=[2]) == "/loans/2/"


def test_pages_use_base_template(client):
    response = client.get("/books/")
    names = [t.name for t in response.templates]
    assert "base.html" in names
    assert "includes/navigation.html" in names
    assert "books/includes/book_card.html" in names


def test_book_detail_shows_title_and_availability(client):
    html = client.get("/books/1/").content.decode()
    assert "Мастер и Маргарита" in html
    assert "свободно" in html


def test_list_uses_length_filter(client):
    assert "Всего книг: 6" in client.get("/books/").content.decode()


def test_loan_status_badges(client):
    html = client.get("/loans/").content.decode()
    assert "Возвращена" in html
    assert "Просрочена" in html


def test_navigation_links_present(client):
    html = client.get("/").content.decode()
    assert 'href="/books/"' in html
    assert 'href="/loans/"' in html


def test_static_files_connected(client):
    html = client.get("/").content.decode()
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/js/main.js" in html
    assert "/static/homepage/img/logo.png" in html
    for name in ("css/style.css", "js/main.js", "img/logo.png"):
        assert (ROOT / "homepage/static/homepage" / name).exists()


def test_views_do_not_build_html_with_page():
    for app in ("homepage", "books", "loans"):
        source = (ROOT / app / "views.py").read_text(encoding="utf-8")
        assert "page(" not in source.replace("render(", "")
        assert "HttpResponse" not in source
