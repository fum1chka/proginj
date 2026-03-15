import pytest
from models import Book, User
from repository import LibraryRepository


class TestBook:
    """Тесты для класса Book"""

    def test_book_creation_and_attributes(self):
        """Тест создания книги и её атрибутов"""
        book = Book(id=1, title="Гарри Поттер", author="Джоан Роулинг")

        assert book.id == 1
        assert book.title == "Гарри Поттер"
        assert book.author == "Джоан Роулинг"
        assert book.available is True


class TestUser:
    """Тесты для класса User"""

    def test_user_creation(self):
        """Тест создания пользователя и его атрибутов"""
        user = User(
            id=1,
            name="Иван Иванов",
            phone="+7-999-000-00-00",
            card_number="AB123456",
        )

        assert user.id == 1
        assert user.name == "Иван Иванов"
        assert user.phone == "+7-999-000-00-00"
        assert user.card_number == "AB123456"
        assert user.borrowed_books == []


class TestLibraryRepository:
    """Тесты для класса LibraryRepository"""

    @pytest.fixture
    def repo(self, tmp_path) -> LibraryRepository:
        """Фикстура репозитория с временной папкой данных"""
        return LibraryRepository(data_dir=tmp_path)

    def test_add_user_and_book_and_issue(self, repo: LibraryRepository):
        """Один сценарий: добавили пользователя, книгу и выдали её"""
        user = repo.add_user(name="Читатель", phone="12345")
        book = repo.add_book(title="Книга", author="Автор")

        # Проверяем, что объекты создались
        assert repo.get_user(user.id) is not None
        assert repo.get_book(book.id) is not None

        # Выдаём книгу
        repo.issue_book_to_user(book, user)

        assert book.available is False
        assert book.id in user.borrowed_books

