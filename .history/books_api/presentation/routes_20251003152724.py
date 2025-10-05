from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from enum import Enum

from books_api.data.database import get_db
from books_api.data.repositories import BookRepository, 
from books_api.presentation.schemas import BookSchema


from books_api.data.repositories import BookHistoryRepository
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from books_api.data.database import get_db

router = APIRouter()

# DRY: repository via Depends
def get_book_repo(db: Session = Depends(get_db)):
    return BookRepository(db)

# Enum pour availability
class Availability(str, Enum):
    in_stock = "In stock"
    out_of_stock = "Out of stock"

# 🔹 Endpoints fixes en premier

# Filtrer par prix
@router.get("/books/price", response_model=List[BookSchema])
def get_books_by_price(
    min_price: float = Query(0, ge=0),
    max_price: float = Query(10000, ge=0),
    repo: BookRepository = Depends(get_book_repo)
):
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price doit être inférieur à max_price")
    return repo.get_by_price_range(min_price, max_price)

# Filtrer par catégorie
@router.get("/books/category/{category}", response_model=List[BookSchema])
def get_books_by_category(category: str, repo: BookRepository = Depends(get_book_repo)):
    return repo.get_by_category(category)

# Filtrer par disponibilité
@router.get("/books/availability/{availability}", response_model=List[BookSchema])
def get_books_by_availability(availability: Availability, repo: BookRepository = Depends(get_book_repo)):
    return repo.get_by_availability(availability.value)

# Endpoint de recherche combinée
@router.get("/books/search", response_model=List[BookSchema])
def search_books(
    category: Optional[str] = None,
    min_price: float = 0,
    max_price: float = 10000,
    availability: Optional[Availability] = None,
    rating: Optional[int] = Query(None, ge=1, le=5),  
    skip: int = 0,
    limit: int = 100,
    repo: BookRepository = Depends(get_book_repo)
):
    # Appel du repository
    results = repo.search(
        category=category,
        min_price=min_price,
        max_price=max_price,
        availability=availability,
        rating=rating,
        skip=skip,
        limit=limit
    )
    return results


# par ucp

@router.get("/books/upc/{upc}", response_model=BookSchema)
def get_book_by_upc(upc: str, repo: BookRepository = Depends(get_book_repo)):
    book = repo.get_by_upc(upc)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book




# Liste tous les livres
@router.get("/books", response_model=List[BookSchema])
def list_books(skip: int = 0, limit: int = 100, repo: BookRepository = Depends(get_book_repo)):
    return repo.get_all(skip, limit)



@router.get("/books/price-history/{upc}")
def get_book_price_history(upc: str, db: Session = Depends(get_db)):
    """
    Retourne l'historique des variations de prix pour un livre.
    """
    repo = BookHistoryRepository(db)
    price_changes = repo.get_price_changes(upc)
    if not price_changes:
        raise HTTPException(status_code=404, detail="Aucune variation de prix trouvée pour ce livre")
    return price_changes


