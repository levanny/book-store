from pydantic import BaseModel

class Book(BaseModel):
    id: int | None = None
    title: str
    author: str
    price: float