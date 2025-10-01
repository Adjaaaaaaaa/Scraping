from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from books_api.data.database import get_db
from books_api.data.repositories import SQLAlchemyBookRepository

router = APIRouter()

# ✅ Tous les livres
@router.get("/books")
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_all(skip, limit)

# ✅ Livre par ID
@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_by_id(book_id)

# ✅ Livre par catégorie
@router.get("/books/category/{category}")
def get_books_by_category(category: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_by_category(category)

# ✅ Livre par prix (min / max)
@router.get("/books/price")
def get_books_by_price(
    min_price: float = Query(0), 
    max_price: float = Query(100), 
    db: Session = Depends(get_db)
):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_by_price_range(min_price, max_price)

# ✅ Livre par disponibilité ("In stock", "Out of stock"...)
@router.get("/books/availability/{availability}")
def get_books_by_availability(availability: str, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_by_availability(availability)

# ✅ Livre par rating (exemple : 1 à 5)
@router.get("/books/rating/{rating}")
def get_books_by_rating(rating: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_by_rating(rating)
