from sqlalchemy.orm import Session
from books_api.domain.models import Book
from .database import Base
from sqlalchemy import Column, Integer, String, Float

# Table SQLAlchemy pour Book
class BookTable(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)

# Repository pour manipuler les livres
class SQLAlchemyBookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip=0, limit=100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()

    def create(self, book: Book):
        db_book = BookTable(
            title=book.title,
            price=book.price,
            availability=book.availability,
            rating=book.rating
        )
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book
