from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float
from books_api.data.database import Base

class BookTable(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    category = Column(String)  # ⚡ doit exister dans ta table SQLite

class SQLAlchemyBookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()

    def get_by_category(self, category: str):
        return self.db.query(BookTable).filter(BookTable.category == category).all()

    def get_by_price_range(self, min_price: float, max_price: float):
        return (
            self.db.query(BookTable)
            .filter(BookTable.price >= min_price, BookTable.price <= max_price)
            .all()
        )

    def get_by_availability(self, availability: str):
        return (
            self.db.query(BookTable)
            .filter(BookTable.availability == availability)
            .all()
        )
