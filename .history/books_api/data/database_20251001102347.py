# books_api/data/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///books_scraper/book.bd"  # chemin vers ta DB existante

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
