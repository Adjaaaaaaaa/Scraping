from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine

# Base SQLAlchemy
Base = declarative_base()

# Connexion SQLite (change en "postgresql://user:pass@localhost/db" si tu veux PostgreSQL)
engine = create_engine("sqlite:///books.db", echo=False)

# Session factory
Session = sessionmaker(bind=engine)


# Table principale des livres
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    category = Column(String)
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


# Historique des modifications
class BookHistory(Base):
    __tablename__ = "book_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_upc = Column(String)
    action = Column(String)  # "added", "updated", "deleted"
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    change_date = Column(DateTime, default=datetime.utcnow)


# Création des tables si elles n’existent pas
Base.metadata.create_all(engine)
