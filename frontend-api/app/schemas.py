from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    firstname: str
    lastname: str
    password: str

class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

class BookResponse(BookBase):
    id: int
    available: bool

    class Config:
        from_attributes = True

class BorrowRequest(BaseModel):
    days: int

class BorrowResponse(BaseModel):
    book: BookResponse
    borrowed_on: datetime
    return_by: datetime

    class Config:
        from_attributes = True
