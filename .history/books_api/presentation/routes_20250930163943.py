from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from books_api.data.database import get_db
from books_api.data.repositories import SQLAlchemyBookRepository
from books_api.presentation import schemas

router = APIRouter()

# Lister tous les livres
@router.get("/books", response_model=list[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_all(skip, limit)

# Lire un livre par id
@router.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
