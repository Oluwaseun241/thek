import pytest
from httpx import AsyncClient
from app.main import app
from database import get_db
from app import models
from bson import ObjectId

# Fixture to setup and teardown test database
@pytest.fixture
def db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()

# Async test client
@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8001") as client:
        yield client

# Test for adding a new book
@pytest.mark.asyncio
async def test_add_new_book(async_client):
    payload = {
        "title": "New Book Title",
        "author": "New Author",
        "publisher": "New Publisher",
        "category": "Technology",
        "is_available": True
    }
    response = await async_client.post("/books/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Book Title"
    assert data["author"] == "New Author"
    assert data["category"] == "Technology"

# Test for removing a book
@pytest.mark.asyncio
async def test_remove_book(async_client, db):
    book_id = ObjectId()
    new_book = models.Book(
        #_id=book_id,
        title="Book to Remove",
        author="Remove Author",
        publisher="Remove Publisher",
        category="Science",
        is_available=True
    )
    db.books.insert_one(new_book.dict())

    response = await async_client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Book removed successfully"

    book = db.books.find_one({"_id": ObjectId(book_id)})
    assert book is None

# Test for listing all users
@pytest.mark.asyncio
async def test_list_users(async_client, db):
    user1 = models.User(
        email="user1@example.com",
        firstname="John",
        lastname="Doe"
    )
    user2 = models.User(
        email="user2@example.com",
        firstname="Jane",
        lastname="Smith"
    )
    db.users.insert_many([user1.dict(), user2.dict()])

    response = await async_client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 2
    assert users[0]["email"] == "user1@example.com"
    assert users[1]["email"] == "user2@example.com"

