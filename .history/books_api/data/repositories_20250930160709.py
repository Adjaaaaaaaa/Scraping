from sqlalchemy.orm import Session
from domain.models import Book
from domain.interfaces import BookRepository
from . import models

class SQLAlchemyBookRepository(BookRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Book]:
        books = self.db.query(models.BookORM).offset(skip).limit(limit).all()
        return [Book(**book.__dict__) for book in books]

    def get_by_id(self, book_id: int) -> Book | None:
        book = self.db.query(models.BookORM).filter(models.BookORM.id == book_id).first()
        return Book(**book.__dict__) if book else None

    def create(self, book: Book) -> Book:
        db_book = models.BookORM(**book.__dict__)
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return Book(**db_book.__dict__)
