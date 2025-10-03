from dataclasses import dataclass

@dataclass
class Book:
    id: int | None
    title: str
    price: float
    availability: str
    rating: int
    category: str
