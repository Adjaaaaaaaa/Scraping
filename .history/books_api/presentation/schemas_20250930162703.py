from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    price: float
    availability: str
    rating: int

class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True
