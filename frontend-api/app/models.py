# SqlAlclchemy Import
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    borrowed_books = relationship('Borrow', back_populates='user')

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String, nullable=False)
    category = Column(String, nullable=False)
    availabe = Column(Boolean, default=True)


class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrowed_on = Column(DateTime, default=datetime.utcnow)
    return_by = Column(DateTime)
    user = relationship('User', back_populates='borrows') 
    book = relationship('Book', back_populates='borrrws')

