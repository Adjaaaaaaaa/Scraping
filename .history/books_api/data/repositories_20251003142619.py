from sqlalchemy.orm import Session
from sqlalchemy import and_
from books_api.data.tables import BookTable

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()
    
    # books_api/data/repositories.py
def get_by_upc(self, upc: str):
    return self.db.query(BookTable).filter(BookTable.upc == upc).first()



    def get_by_category(self, category: str):
        return self.db.query(BookTable).filter(BookTable.category == category).all()

    def get_by_price_range(self, min_price: float, max_price: float):
        return self.db.query(BookTable).filter(
            and_(BookTable.price >= min_price, BookTable.price <= max_price)
        ).all()

    def get_by_availability(self, availability: str):
        return self.db.query(BookTable).filter(BookTable.availability == availability).all()

    # Search with combined filters
    def search(self, category=None, min_price=0, max_price=10000, availability=None, skip=0, limit=100, rating=None):
        query = self.db.query(BookTable)
        
        if category:
            query = query.filter(BookTable.category == category)
        
        if availability:
            query = query.filter(BookTable.availability == availability)
        
        if rating:
            query = query.filter(BookTable.rating == rating)  # filtre par rating
        
        query = query.filter(BookTable.price >= min_price, BookTable.price <= max_price)
        return query.offset(skip).limit(limit).all()
