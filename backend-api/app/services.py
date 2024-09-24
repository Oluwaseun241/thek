from bson import ObjectId
from pymongo.collection import Collection
from models import Book, User


def create_book(collection: Collection, book: Book):
    book_dict = book.dict(by_alias=True)
    result = collection.insert_one(book_dict)
    book.id = result.inserted_id
    return book


def remove_book(collection: Collection, book_id: str):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0


def get_books(collection: Collection):
    books = list(collection.find())
    return [Book(**book) for book in books]


def get_users(collection: Collection):
    users = list(collection.find())
    return [User(**user) for user in users]
