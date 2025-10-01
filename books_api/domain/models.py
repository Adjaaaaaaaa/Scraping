# books_api/domain/models.py
from dataclasses import dataclass

@dataclass
class Book:
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str
