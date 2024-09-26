import pytest
from httpx import AsyncClient
from app.main import app
from app.database import get_db, SessionLocal
from app import models

@pytest.fixture
def db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client

# Test for user enrollment
@pytest.mark.asyncio
async def test_user_enrollment(async_client):
    payload = {
        "email": "testuser@example.com",
        "firstname": "John",
        "lastname": "Doe"
    }
    response = await async_client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["firstname"] == "John"
    assert data["lastname"] == "Doe"

# Test for listing available books
@pytest.mark.asyncio
async def test_list_available_books(async_client, db):
    new_book = models.Book(
        title="Test Book",
        author="Test Author",
        publisher="Test Publisher",
        category="Fiction",
        is_available=True
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    response = await async_client.get("/books/")
    assert response.status_code == 200
    books = response.json()
    assert len(books) > 0
    assert books[0]["title"] == "Test Book"

# Test for borrowing a book
@pytest.mark.asyncio
async def test_borrow_book(async_client, db):
    new_book = models.Book(
        title="Borrow Test Book",
        author="Borrow Author",
        publisher="Borrow Publisher",
        category="Fiction",
        is_available=True
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    response = await async_client.post(f"/books/{new_book.id}/borrow", json={"days": 7})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Book borrowed successfully"

    response = await async_client.get("/books/")
    books = response.json()
    borrowed_book = next((book for book in books if book["id"] == new_book.id), None)
    assert borrowed_book["is_available"] == False

