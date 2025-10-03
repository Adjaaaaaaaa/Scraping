# books_api/data/tables.py
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class BookTable(Base):
    __tablename__ = "books"  # exact nom de ta table existante

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    category = Column(String)
