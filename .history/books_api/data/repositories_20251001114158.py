# books_api/data/repositories.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from .tables import BookTable

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()

    def get_by_category(self, category: str):
        return self.db.query(BookTable).filter(BookTable.category == category).all()

    def get_by_price_range(self, min_price: float, max_price: float):
        return self.db.query(BookTable).filter(
            and_(BookTable.price >= min_price, BookTable.price <= max_price)
        ).all()

    def get_by_availability(self, availability: str):
        return self.db.query(BookTable).filter(BookTable.availability == availability).all()


@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = BookRepository(db)
    return repo.get_by_id(book_id)
