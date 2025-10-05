from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base pour SQLAlchemy
Base = declarative_base()

# --------------------------
# Table principale : Book
# --------------------------
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    category = Column(String)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    url = Column(String)
    copies_available = Column(Integer)
    upc = Column(String, unique=True)
    price_excl_tax = Column(Float)
    price_incl_tax = Column(Float)
    tax = Column(Float)
    num_reviews = Column(Integer)

# --------------------------
# Table d’historique : BookHistory
# --------------------------
class BookHistory(Base):
    __tablename__ = "book_history"

    id = Column(Integer, primary_key=True, index=True)
    book_upc = Column(String, index=True)
    action = Column(String)  # "added", "updated", "deleted"
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    change_date = Column(DateTime, default=datetime.utcnow)
