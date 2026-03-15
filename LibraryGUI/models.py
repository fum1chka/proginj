from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Book:
    id: int
    title: str
    author: str
    available: bool = True


@dataclass
class User:
    id: int
    name: str
    phone: Optional[str] = None
    card_number: Optional[str] = None
    borrowed_books: List[int] = field(default_factory=list)

