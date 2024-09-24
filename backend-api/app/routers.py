from fastapi import APIRouter, HTTPException
import services, schemas, database, messaging
from models import Book, User

router = APIRouter()


@router.post("/books", response_model=schemas.Book)
def add_book(book: schemas.BookCreate):
    new_book = Book(**book.dict())
    created_book = services.create_book(database.books_collection, new_book)
    messaging.send_message("Book added", str(created_book.id))
    return created_book


@router.delete("/books/{book_id}")
def delete_book(book_id: str):
    success = services.remove_book(database.books_collection, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    messaging.send_message("Book removed", book_id)
    return {"message": "Book removed successfully"}


@router.get("/users", response_model=list[schemas.User])
def list_users():
    return services.get_users(database.users_collection)


@router.get("/books", response_model=list[schemas.Book])
def list_books():
    return services.get_books(database.books_collection)

