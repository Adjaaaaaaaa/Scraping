class SQLAlchemyBookRepository:
    def __init__(self, db):
        self.db = db

    def get_all(self, skip=0, limit=100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()

    def get_by_price_range(self, min_price: float, max_price: float):
        return self.db.query(BookTable).filter(BookTable.price.between(min_price, max_price)).all()

    def get_by_availability(self, availability: str):
        return self.db.query(BookTable).filter(BookTable.availability == availability).all()

    def get_by_rating(self, rating: int):
        return self.db.query(BookTable).filter(BookTable.rating == rating).all()
oui