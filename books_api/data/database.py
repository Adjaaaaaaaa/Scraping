from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database connection URL
DATABASE_URL = "sqlite:///C:/Users/adjah/Desktop/Simplon/projets simplon/Scraping/books.db"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}  # obligatoire pour SQLite
)
# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency pour FastAPI
def get_db():
    """
    Dependency function for FastAPI routes.
    
    Provides a database session to endpoints and ensures it is closed after use.
    
    Yields:
        Session: SQLAlchemy session object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


