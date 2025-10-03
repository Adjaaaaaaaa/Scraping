from pydantic import BaseModel
from typing import Optional

class BookSchema(BaseModel):
    id: int
    title: str
    category: str
    price: float
    availability: str
    rating: int
    url: Optional[str]
    copies_available: Optional[int]
    upc: Optional[str]
    price_excl_tax: Optional[float]
    price_incl_tax: Optional[float]
    tax: Optional[float]
    num_reviews: Optional[int]

    class Config:
        orm_mode = True
