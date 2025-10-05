from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
"""
SQLAlchemy models for storing books and their history.

This module defines the tables for the main book data (Book) and
the historical changes (BookHistory) in the SQLite database.
"""

Base = declarative_base()

class Book(Base):
    """
    Main table representing a book.

    Attributes:
        id (int): Primary key
        title (str): Book title
        category (str): Book category
        price (float): Current price
        availability (str): Availability status
        rating (int): Star rating (1-5)
        url (str): URL of the book page
        copies_available (int): Number of copies available
        upc (str): Unique product code
        price_excl_tax (float): Price excluding tax
        price_incl_tax (float): Price including tax
        tax (float): Tax amount
        num_reviews (int): Number of reviews
    """
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

class BookHistory(Base):
    """
    Table for storing historical changes to books.

    Attributes:
        id (int): Primary key
        book_upc (str): Reference to the book's UPC
        action (str): Type of change ("added", "updated", "deleted")
        old_data (JSON): Previous state of the book (nullable)
        new_data (JSON): New state of the book (nullable)
        change_date (datetime): Timestamp of the change
    """
    __tablename__ = "book_history"

    id = Column(Integer, primary_key=True, index=True)
    book_upc = Column(String, index=True)
    action = Column(String)  # "added", "updated", "deleted"
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    change_date = Column(DateTime, default=datetime.utcnow)
