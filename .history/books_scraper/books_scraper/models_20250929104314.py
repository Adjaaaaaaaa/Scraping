from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Base pour SQLAlchemy
Base = declarative_base()

# Connexion à la base SQLite (fichier books.db)
engine = create_engine("sqlite:///books.db")

# Définition de la table "books"
class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True)
    title = Column(String)        # Titre du livre
    price = Column(Float)         # Prix en float
    availability = Column(String) # "In stock" / "Out of stock"
    rating = Column(Integer)      # Note (1 à 5)
    category = Column(String)     # Catégorie du livre

# Crée la table si elle n’existe pas déjà
Base.metadata.create_all(engine)
