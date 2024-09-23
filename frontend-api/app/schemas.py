from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    firstname: str
    lastname: str

class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

class BookResponse(BookBase):
    id: int
    available: bool

    class Config:
        orm_mode = True

class BorrowRequest(BaseModel):
    days: int

class BorrowResponse(BaseModel):
    book: BookResponse
    borrowed_on: datetime
    return_by: datetime

    class Config:
        orm_mode = True
