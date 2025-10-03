from sqlalchemy.orm import Session
from books_api.domain.models import Book
from .database import Base
from sqlalchemy import Column, Integer, String, Float

# Table SQLAlchemy pour mapper les livres existants
class BookTable(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)

# Repository pour accéder aux livres
class SQLAlchemyBookRepository:
    def __init__(self, db: Session):
        self.db = db

    # Retourne tous les livres avec pagination
    def get_all(self, skip: int = 0, limit: int = 100) -> list[BookTable]:
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    # Retourne un livre spécifique par ID
    def get_by_id(self, book_id: int) -> BookTable | None:
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()

    # Fonction pour filtrer les livres par prix ou rating si nécessaire
    def filter_books(self, min_price: float = 0, max_price: float = 1e6, min_rating: int = 0) -> list[BookTable]:
        query = self.db.query(BookTable).filter(
            BookTable.price >= min_price,
            BookTable.price <= max_price,
            BookTable.rating >= min_rating
        )
        return query.all()
