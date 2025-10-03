from pydantic import BaseModel

class BookModel(BaseModel):
    id: int | None
    title: str
    price: float
    availability: str
    rating: int
    category: str

    class Config:
        from_attributes = True  # mappe automatiquement BookORM
