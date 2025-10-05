from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from enum import Enum
from books_api.data.database import get_db
from books_api.data.repositories import BookRepository, BookHistoryRepository
from books_api.presentation.schemas import BookSchema


router = APIRouter()

def get_book_repo(db: Session = Depends(get_db)):
    """
    Returns a BookRepository instance using the current database session.
    This allows endpoints to remain DRY.
    """
    return BookRepository(db)

class Availability(str, Enum):
    """
    Enum for book availability status.
    """
    in_stock = "In stock"
    out_of_stock = "Out of stock"

@router.get("/books/price", response_model=List[BookSchema])
def get_books_by_price(
    min_price: float = Query(0, ge=0),
    max_price: float = Query(10000, ge=0),
    repo: BookRepository = Depends(get_book_repo)
):
    """
    Retrieve books within a given price range.

    - **min_price**: minimum price (inclusive)
    - **max_price**: maximum price (inclusive)
    """
    if min_price > max_price:
        raise HTTPException(status_code=400, detail="min_price doit être inférieur à max_price")
    return repo.get_by_price_range(min_price, max_price)

@router.get("/books/category/{category}", response_model=List[BookSchema])
def get_books_by_category(category: str, repo: BookRepository = Depends(get_book_repo)):
    """
    Retrieve all books of a given category.
    """   
    return repo.get_by_category(category)

@router.get("/books/availability/{availability}", response_model=List[BookSchema])
def get_books_by_availability(availability: Availability, repo: BookRepository = Depends(get_book_repo)):
    """
    Retrieve books by availability status.
    """   
    return repo.get_by_availability(availability.value)

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
    """
    Search for books using multiple optional filters:
    
    - **category**: filter by category
    - **min_price** / **max_price**: filter by price range
    - **availability**: filter by stock status
    - **rating**: filter by star rating (1-5)
    - **skip** / **limit**: pagination
    """

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


@router.get("/books/upc/{upc}", response_model=BookSchema)
def get_book_by_upc(upc: str, repo: BookRepository = Depends(get_book_repo)):
    """
    Retrieve a single book by its unique UPC.
    """   
    book = repo.get_by_upc(upc)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.get("/books", response_model=List[BookSchema])
def list_books(skip: int = 0, limit: int = 100, repo: BookRepository = Depends(get_book_repo)):
    """
    List all books with optional pagination.
    """   
    return repo.get_all(skip, limit)



@router.get("/books/price-history/{upc}")
def get_book_price_history(upc: str, db: Session = Depends(get_db)):
    """
    Retrieve the price change history for a specific book by UPC.
    
    Returns a list of price change records containing:
    - change_date
    - old_price
    - new_price
    - action (added/updated/deleted)
    """
    repo = BookHistoryRepository(db)
    price_changes = repo.get_price_changes(upc)
    if not price_changes:
        raise HTTPException(status_code=404, detail="Aucune variation de prix trouvée pour ce livre")
    return price_changes


