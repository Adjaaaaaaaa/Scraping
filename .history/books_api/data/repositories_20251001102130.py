# books_api/data/repositories.py
from sqlalchemy.orm import Session
from books_api.domain.models import Book
from sqlalchemy import select, and_

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        result = self.db.execute(select(Book)).scalars().all()
        return result[skip : skip + limit]

    def get_by_id(self, book_id: int):
        result = self.db.execute(select(Book).where(Book.id == book_id)).scalar_one_or_none()
        return result

    def get_by_category(self, category: str):
        result = self.db.execute(select(Book).where(Book.category == category)).scalars().all()
        return result

    def get_by_price_range(self, min_price: float, max_price: float):
        result = self.db.execute(
            select(Book).where(and_(Book.price >= min_price, Book.price <= max_price))
        ).scalars().all()
        return result

    def get_by_availability(self, availability: str):
        result = self.db.execute(select(Book).where(Book.availability == availability)).scalars().all()
        return result
