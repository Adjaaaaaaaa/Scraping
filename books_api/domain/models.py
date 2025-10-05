from dataclasses import dataclass

@dataclass
class Book:
    """
    Dataclass representing a book entity.

    This class is used to define the structure of book objects
    within the application domain or for API responses.
    """
    id: int
    title: str
    price: float
    availability: str
    rating: int
    category: str
