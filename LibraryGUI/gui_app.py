import tkinter as tk
from tkinter import messagebox, ttk

from models import Book, User
from repository import LibraryRepository


class LibraryGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Информационная система 'Библиотека'")
        self.geometry("800x500")
        self.resizable(False, False)

        self.repo = LibraryRepository()
        self.current_user: User | None = None

        self._build_ui()

    # --- UI construction ---
    def _build_ui(self) -> None:
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.reader_frame = ttk.Frame(nb)
        self.librarian_frame = ttk.Frame(nb)

        nb.add(self.reader_frame, text="Читатель")
        nb.add(self.librarian_frame, text="Библиотекарь")

        self._build_reader_tab()
        self._build_librarian_tab()

    # --- Reader tab ---
    def _build_reader_tab(self) -> None:
        frame = self.reader_frame

        # Текущий пользователь
        top = ttk.Frame(frame)
        top.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(top, text="Текущий пользователь:").pack(side=tk.LEFT)
        self.current_user_label = ttk.Label(top, text="нет")
        self.current_user_label.pack(side=tk.LEFT, padx=(5, 0))

        # Регистрация
        reg_frame = ttk.LabelFrame(frame, text="Регистрация")
        reg_frame.pack(fill=tk.X, pady=(0, 10))

        # По телефону
        phone_frame = ttk.Frame(reg_frame)
        phone_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(phone_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.entry_reg_phone_name = ttk.Entry(phone_frame, width=25)
        self.entry_reg_phone_name.grid(row=0, column=1, padx=5)

        ttk.Label(phone_frame, text="Телефон:").grid(row=0, column=2, sticky="w")
        self.entry_reg_phone_phone = ttk.Entry(phone_frame, width=20)
        self.entry_reg_phone_phone.grid(row=0, column=3, padx=5)

        ttk.Button(
            phone_frame,
            text="Регистрация по телефону",
            command=self.register_user_by_phone,
        ).grid(row=0, column=4, padx=5)

        # По читательскому билету
        card_frame = ttk.Frame(reg_frame)
        card_frame.pack(fill=tk.X, pady=5, padx=5)

        ttk.Label(card_frame, text="Имя:").grid(row=0, column=0, sticky="w")
        self.entry_reg_card_name = ttk.Entry(card_frame, width=25)
        self.entry_reg_card_name.grid(row=0, column=1, padx=5)

        ttk.Label(card_frame, text="№ билета:").grid(row=0, column=2, sticky="w")
        self.entry_reg_card_number = ttk.Entry(card_frame, width=20)
        self.entry_reg_card_number.grid(row=0, column=3, padx=5)

        ttk.Button(
            card_frame,
            text="Регистрация по билету",
            command=self.register_user_by_card,
        ).grid(row=0, column=4, padx=5)

        # Вход
        login_frame = ttk.LabelFrame(frame, text="Вход в систему")
        login_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(login_frame, text="ID пользователя:").pack(side=tk.LEFT, padx=5, pady=5)
        self.entry_login_id = ttk.Entry(login_frame, width=10)
        self.entry_login_id.pack(side=tk.LEFT, padx=5)
        ttk.Button(login_frame, text="Войти", command=self.login).pack(side=tk.LEFT, padx=5)

        # Поиск и выдача
        search_frame = ttk.LabelFrame(frame, text="Поиск и выдача книги")
        search_frame.pack(fill=tk.BOTH, expand=True)

        search_top = ttk.Frame(search_frame)
        search_top.pack(fill=tk.X, padx=5, pady=5)

        self.search_var = tk.StringVar(value="title")
        ttk.Radiobutton(
            search_top, text="По названию", variable=self.search_var, value="title"
        ).pack(side=tk.LEFT)
        ttk.Radiobutton(
            search_top, text="По автору", variable=self.search_var, value="author"
        ).pack(side=tk.LEFT, padx=(10, 0))

        self.entry_search_query = ttk.Entry(search_top, width=40)
        self.entry_search_query.pack(side=tk.LEFT, padx=10)

        ttk.Button(search_top, text="Искать", command=self.search_books).pack(
            side=tk.LEFT
        )

        # Результаты поиска
        self.search_tree = ttk.Treeview(
            search_frame,
            columns=("id", "title", "author", "status"),
            show="headings",
            height=8,
        )
        self.search_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.search_tree.heading("id", text="ID")
        self.search_tree.heading("title", text="Название")
        self.search_tree.heading("author", text="Автор")
        self.search_tree.heading("status", text="Статус")

        self.search_tree.column("id", width=50, anchor="center")
        self.search_tree.column("title", width=250)
        self.search_tree.column("author", width=200)
        self.search_tree.column("status", width=80, anchor="center")

        issue_frame = ttk.Frame(search_frame)
        issue_frame.pack(fill=tk.X, padx=5, pady=(0, 5))

        ttk.Label(issue_frame, text="ID для выдачи:").pack(side=tk.LEFT)
        self.entry_issue_id = ttk.Entry(issue_frame, width=10)
        self.entry_issue_id.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            issue_frame,
            text="Выдать книгу текущему читателю",
            command=self.issue_book,
        ).pack(side=tk.LEFT, padx=5)

    # --- Librarian tab ---
    def _build_librarian_tab(self) -> None:
        frame = self.librarian_frame

        add_frame = ttk.LabelFrame(frame, text="Добавление книги")
        add_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Label(add_frame, text="Название:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_book_title = ttk.Entry(add_frame, width=40)
        self.entry_book_title.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Автор:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.entry_book_author = ttk.Entry(add_frame, width=30)
        self.entry_book_author.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(
            add_frame,
            text="Добавить книгу",
            command=self.add_book,
        ).grid(row=0, column=4, padx=5, pady=5)

        list_frame = ttk.LabelFrame(frame, text="Все книги в системе")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        self.books_tree = ttk.Treeview(
            list_frame,
            columns=("id", "title", "author", "status"),
            show="headings",
            height=12,
        )
        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.books_tree.heading("id", text="ID")
        self.books_tree.heading("title", text="Название")
        self.books_tree.heading("author", text="Автор")
        self.books_tree.heading("status", text="Статус")

        self.books_tree.column("id", width=50, anchor="center")
        self.books_tree.column("title", width=250)
        self.books_tree.column("author", width=200)
        self.books_tree.column("status", width=80, anchor="center")

        ttk.Button(
            list_frame,
            text="Обновить список книг",
            command=self.refresh_books_list,
        ).pack(side=tk.BOTTOM, pady=(0, 5))

        self.refresh_books_list()

    # --- Reader actions ---
    def register_user_by_phone(self) -> None:
        name = self.entry_reg_phone_name.get().strip()
        phone = self.entry_reg_phone_phone.get().strip()
        if not name or not phone:
            messagebox.showwarning("Ошибка", "Имя и телефон не могут быть пустыми.")
            return
        user = self.repo.add_user(name=name, phone=phone)
        messagebox.showinfo(
            "Успех",
            f"Пользователь зарегистрирован.\nID: {user.id}",
        )
        self.entry_reg_phone_name.delete(0, tk.END)
        self.entry_reg_phone_phone.delete(0, tk.END)

    def register_user_by_card(self) -> None:
        name = self.entry_reg_card_name.get().strip()
        card_number = self.entry_reg_card_number.get().strip()
        if not name or not card_number:
            messagebox.showwarning(
                "Ошибка", "Имя и номер читательского билета не могут быть пустыми."
            )
            return
        user = self.repo.add_user(name=name, card_number=card_number)
        messagebox.showinfo(
            "Успех",
            f"Пользователь зарегистрирован.\nID: {user.id}",
        )
        self.entry_reg_card_name.delete(0, tk.END)
        self.entry_reg_card_number.delete(0, tk.END)

    def login(self) -> None:
        if not self.repo.has_users():
            messagebox.showinfo(
                "Информация", "Нет зарегистрированных пользователей. Сначала выполните регистрацию."
            )
            return
        raw = self.entry_login_id.get().strip()
        try:
            user_id = int(raw)
        except ValueError:
            messagebox.showerror("Ошибка", "ID пользователя должен быть числом.")
            return
        user = self.repo.get_user(user_id)
        if not user:
            messagebox.showerror("Ошибка", "Пользователь с таким ID не найден.")
            return
        self.current_user = user
        self.current_user_label.config(text=user.name)
        messagebox.showinfo("Вход выполнен", f"Вы вошли как: {user.name}")

    def _require_logged_in(self) -> bool:
        if not self.current_user:
            messagebox.showwarning(
                "Требуется вход",
                "Поиск и выдача книг доступны только авторизованным пользователям.",
            )
            return False
        return True

    def search_books(self) -> None:
        if not self._require_logged_in():
            return

        query = self.entry_search_query.get().strip().lower()
        if not query:
            messagebox.showwarning("Ошибка", "Введите строку для поиска.")
            return

        mode = self.search_var.get()
        all_books = self.repo.list_books()
        if mode == "title":
            results = [b for b in all_books if query in b.title.lower()]
        else:
            results = [b for b in all_books if query in b.author.lower()]

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

        if not results:
            messagebox.showinfo(
                "Не найдено",
                "Книга не найдена.\nСообщение: Желаемая книга отсутствует в системе.",
            )
            return

        for book in results:
            status = "доступна" if book.available else "выдана"
            self.search_tree.insert(
                "",
                tk.END,
                values=(book.id, book.title, book.author, status),
            )

    def issue_book(self) -> None:
        if not self._require_logged_in():
            return

        raw = self.entry_issue_id.get().strip()
        if not raw:
            messagebox.showwarning("Ошибка", "Введите ID книги для выдачи.")
            return
        try:
            book_id = int(raw)
        except ValueError:
            messagebox.showerror("Ошибка", "ID книги должен быть числом.")
            return

        book = self.repo.get_book(book_id)
        if not book:
            messagebox.showerror("Ошибка", "Книга с таким ID не найдена.")
            return
        if not book.available:
            messagebox.showinfo("Информация", "Книга уже выдана другому читателю.")
            return

        self.repo.issue_book_to_user(book, self.current_user)  # type: ignore[arg-type]
        messagebox.showinfo(
            "Успех",
            f"Книга '{book.title}' выдана читателю {self.current_user.name}.",  # type: ignore[union-attr]
        )
        self.entry_issue_id.delete(0, tk.END)
        self.refresh_books_list()
        self.search_books()

    # --- Librarian actions ---
    def add_book(self) -> None:
        title = self.entry_book_title.get().strip()
        author = self.entry_book_author.get().strip()
        if not title or not author:
            messagebox.showwarning(
                "Ошибка", "Название и автор книги не могут быть пустыми."
            )
            return
        book = self.repo.add_book(title=title, author=author)
        messagebox.showinfo(
            "Успех",
            f"Книга добавлена.\nID: {book.id}",
        )
        self.entry_book_title.delete(0, tk.END)
        self.entry_book_author.delete(0, tk.END)
        self.refresh_books_list()

    def refresh_books_list(self) -> None:
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)
        for book in self.repo.list_books():
            status = "доступна" if book.available else "выдана"
            self.books_tree.insert(
                "",
                tk.END,
                values=(book.id, book.title, book.author, status),
            )


def run() -> None:
    app = LibraryGUI()
    app.mainloop()

