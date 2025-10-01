class SQLAlchemyBookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip=0, limit=100):
        return self.db.query(BookTable).offset(skip).limit(limit).all()

    def get_by_id(self, book_id: int):
        return self.db.query(BookTable).filter(BookTable.id == book_id).first()
