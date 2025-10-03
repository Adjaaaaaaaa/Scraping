# books_api/data/tables.py
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class BookTable(Base):
    __tablename__ = "books"  # correspond à la table existante du scraper

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    url = Column(String)
    copies_available = Column(Integer)
    upc = Column(String, unique=True, index=True)
    price_excl_tax = Column(Float)
    price_incl_tax = Column(Float)
    tax = Column(Float)
    num_reviews = Column(Integer)
