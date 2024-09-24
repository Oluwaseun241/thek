from pydantic import BaseModel


class BookBase(BaseModel):
    title: str
    author: str
    publisher: str
    category: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: str
    is_available: bool


class User(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
