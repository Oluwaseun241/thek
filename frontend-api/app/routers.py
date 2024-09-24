# FastAPI Imports
from fastapi import APIRouter, Depends, HTTPException, status

# SqlAlchemy Import
from sqlalchemy.orm import Session

# Own Import
from . import schemas, services, database

router = APIRouter()

@router.post("/users", response_model=schemas.UserCreate)
def enroll_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return services.create_user(db, user)

@router.get("/books", response_model=list[schemas.BookResponse])
def list_books(db: Session = Depends(database.get_db)):
    return services.get_books(db)

@router.get("/books/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    book = services.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book

@router.get("/books/filter", response_model=list[schemas.BookResponse])
def filter_books(publisher: str = None, category: str = None, db: Session = Depends(database.get_db)):
    return services.filter_books(db, publisher, category)

@router.post("/books/{book_id}/borrow", response_model=schemas.BorrowResponse)
def borrow_book(book_id: int, borrow: schemas.BorrowRequest, db: Session = Depends(database.get_db)):
    borrow_record = services.borrow_book(db, user_id=1, book_id=book_id, days=borrow.days)  # Hardcoded user_id
    if not borrow_record:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available for borrowing")
    return borrow_record
