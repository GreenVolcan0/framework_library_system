import pytest

from models.readers import Reader, add_reader, find_reader_by_id
from models.users import User


def test_reader_is_a_user():
    reader = Reader(1, "Иванов Пётр", "ivanov@example.com")
    assert isinstance(reader, User)


def test_reader_gets_card_number():
    assert Reader(12, "Иванов", "i@example.com").card_number == "LB-0012"


def test_invalid_email_is_rejected():
    with pytest.raises(ValueError):
        User(1, "Иванов", "no-at-sign")


def test_str_is_polymorphic():
    user = User(1, "Иванов", "i@example.com")
    reader = Reader(1, "Иванов", "i@example.com")
    assert str(user) == "Иванов <i@example.com>"
    assert "LB-0001" in str(reader)


def test_add_and_find_reader():
    readers = []
    reader = add_reader(readers, "Смирнова", "s@example.com")
    assert find_reader_by_id(readers, reader.id) is reader
    assert find_reader_by_id(readers, 99) is None
