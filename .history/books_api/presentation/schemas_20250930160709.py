from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    price: float
    availability: str
    rating: int
    category: str

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    class Config:
        orm_mode = True
