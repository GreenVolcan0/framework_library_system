import pytest
from django.test import Client


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
    assert client.get(url).status_code == 404


def test_book_detail_shows_title_and_availability(client):
    html = client.get("/books/1/").content.decode()
    assert "Мастер и Маргарита" in html
    assert "Свободно" in html


def test_navigation_links_present(client):
    html = client.get("/").content.decode()
    assert 'href="/books/"' in html
    assert 'href="/loans/"' in html
