from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from books_api.data.database import SessionLocal
from books_api.domain.models import Book


from books_api.data.database import get_db
from data.repositories import SQLAlchemyBookRepository
from domain.models import Book
from . import schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/books", response_model=list[schemas.BookResponse])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.get_all(skip, limit)

@router.get("/books/{book_id}", response_model=schemas.BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    book = repo.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    repo = SQLAlchemyBookRepository(db)
    return repo.create(Book(id=None, **book.dict()))
