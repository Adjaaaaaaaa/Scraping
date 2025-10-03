# books_api/data/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = "sqlite:///C:/Users/adjah/Desktop/Simplon/projets simplon/Scraping/books_scraper/books."


engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # obligatoire pour SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if not os.path.exists("C:/Users/adjah/Desktop/Simplon/projets simplon/Scraping/books_scraper/books.db"):
    raise FileNotFoundError("La base de données books.bd n'existe pas à l'emplacement indiqué.")
