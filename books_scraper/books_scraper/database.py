import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

"""
Database connection and initialization module for the Scrapy project.

This module sets up a connection to the SQLite database and provides a session
factory for database operations. It also allows creating tables if they do not exist.
"""

# Absolute path to the project root (Scraping/) 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "books.db")

# Database connection
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
# Session factory 
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """
    Initialize the database by creating all tables defined in models if they don't exist.
    
    This function should be called at the start of the application to ensure
    the database schema is in place.
    """
    Base.metadata.create_all(bind=engine)
