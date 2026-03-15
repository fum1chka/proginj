import json
from pathlib import Path
from typing import Dict, List, Optional

from models import Book, User


class LibraryRepository:
    """
    Репозиторий для хранения данных о книгах и пользователях.
    Данные хранятся в JSON-файле внутри папки проекта.
    При изменении данных происходит автоматическое сохранение.
    """

    def __init__(self, data_dir: Optional[Path] = None) -> None:
        base_dir = Path(__file__).resolve().parent
        self._data_dir = data_dir or base_dir / "data"
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._data_file = self._data_dir / "library_data.json"

        self._users: Dict[int, User] = {}
        self._books: Dict[int, Book] = {}
        self._next_user_id: int = 1
        self._next_book_id: int = 1

        self._load()

    # --- Вспомогательные методы загрузки/сохранения ---
    def _load(self) -> None:
        if not self._data_file.exists():
            return

        try:
            with self._data_file.open("r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            return

        users_raw = raw.get("users", [])
        books_raw = raw.get("books", [])

        for u in users_raw:
            user = User(
                id=u["id"],
                name=u["name"],
                phone=u.get("phone"),
                card_number=u.get("card_number"),
                borrowed_books=u.get("borrowed_books", []),
            )
            self._users[user.id] = user

        for b in books_raw:
            book = Book(
                id=b["id"],
                title=b["title"],
                author=b["author"],
                available=b.get("available", True),
            )
            self._books[book.id] = book

        if self._users:
            self._next_user_id = max(self._users.keys()) + 1
        if self._books:
            self._next_book_id = max(self._books.keys()) + 1

    def _save(self) -> None:
        data = {
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "phone": u.phone,
                    "card_number": u.card_number,
                    "borrowed_books": list(u.borrowed_books),
                }
                for u in self._users.values()
            ],
            "books": [
                {
                    "id": b.id,
                    "title": b.title,
                    "author": b.author,
                    "available": b.available,
                }
                for b in self._books.values()
            ],
        }
        with self._data_file.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # --- Пользователи ---
    def add_user(
        self,
        name: str,
        phone: Optional[str] = None,
        card_number: Optional[str] = None,
    ) -> User:
        user = User(
            id=self._next_user_id,
            name=name,
            phone=phone,
            card_number=card_number,
        )
        self._users[user.id] = user
        self._next_user_id += 1
        self._save()
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def has_users(self) -> bool:
        return bool(self._users)

    def list_users(self) -> List[User]:
        return list(self._users.values())

    # --- Книги ---
    def add_book(self, title: str, author: str) -> Book:
        book = Book(id=self._next_book_id, title=title, author=author)
        self._books[book.id] = book
        self._next_book_id += 1
        self._save()
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        return self._books.get(book_id)

    def list_books(self) -> List[Book]:
        return list(self._books.values())

    def issue_book_to_user(self, book: Book, user: User) -> None:
        book.available = False
        user.borrowed_books.append(book.id)
        self._save()

