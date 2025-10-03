from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

# Base pour SQLAlchemy
Base = declarative_base()

# Connexion à la base SQLite (fichier books.db)
engine = create_engine("sqlite:///books.db")

# Définition de la table "books"
class Book(Base):
    __tablename__ = "books"
    


# Crée la table si elle n’existe pas déjà
Base.metadata.create_all(engine)
