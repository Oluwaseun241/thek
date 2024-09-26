# SqlAlchemy Import
from sqlalchemy.orm import Session

# FastAPI Import
from fastapi import HTTPException, status
from datetime import datetime, timedelta
    
# Own imports
import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    # Check if user exist
    existing_user = db.query(models.User).filter(models.User.email == user.email)
    if existing_user:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    db_user = models.User(email=user.email, fisrtname=user.firstname, lastname=user.lastname, password=user.password)

    db.add(db_user)
    db.commit()

    return {"user": db_user}

def get_books(db: Session):
    return db.query(models.Book).filter(models.Book.availabe == True).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def filter_books(db: Session, publisher: str, category: str):
    query = db.query(models.Book).filter(models.Book.availabe == True)
    if publisher:
        query = query.filter(models.Book.publisher == publisher)
    if category:
        query = query.filter(models.Book.category == category)

    return query.all()


def borrow_book(db:Session, user_id: int, book_id:int, days:int):
    book = get_book_by_id(db,book_id)
    if book and book.availabe:
        book.availabe = False
        borrow = models.Borrow(
            user_id=user_id,
            book_id=book_id,
            return_by=datetime.utcnow() + timedelta(days=days)
        )
        db.add(borrow)
        db.commit()
        return borrow
    return None
