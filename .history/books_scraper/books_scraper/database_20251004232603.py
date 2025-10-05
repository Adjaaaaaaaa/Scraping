import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# --- Chemin absolu vers la racine du projet (Scraping/) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "books.db")

# --- Connexion à la base ---
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    """Créer les tables si elles n'existent pas."""
    Base.metadata.create_all(bind=engine)
