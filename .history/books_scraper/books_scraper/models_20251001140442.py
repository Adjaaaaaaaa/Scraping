from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Base pour SQLAlchemy
Base = declarative_base()

# Connexion à la base SQLite (fichier books.db)
engine = create_engine("sqlite:///books.db")

# Définition de la table "books"
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    category = Column(String)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    url = Column(String)  # lien vers la fiche du livre
    copies_available = Column(Integer)
    upc = Column(String)
    price_excl_tax = Column(String)
    price_incl_tax = Column(String)
    tax = Column(String)
    num_reviews = Column(Integer)

# Crée la table si elle n’existe pas déjà
Base.metadata.create_all(engine)

class BookHistory(Base):
    __tablename__ = "book_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_upc = Column(String)
    action = Column(String)  # "added", "updated", "deleted"
    old_data = Column(JSON, nullable=True)
    new_data = Column(JSON, nullable=True)
    change_date = Column(DateTime, default=datetime.utcnow)