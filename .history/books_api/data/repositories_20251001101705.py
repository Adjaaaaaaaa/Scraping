from sqlalchemy.orm import Session
from .tables import BookORM
from domain.models import BookModel

class SQLAlchemyBookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(BookORM).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookORM).filter(BookORM.id == book_id).first()

    def get_by_category(self, category: str):
        return self.db.query(BookORM).filter(BookORM.category == category).all()

    def get_by_price_range(self, min_price: float = 0, max_price: float = 100):
        return self.db.query(BookORM).filter(BookORM.price.between(min_price, max_price)).all()

    def get_by_availability(self, availability: str):
        return self.db.query(BookORM).filter(BookORM.availability == availability).all()
