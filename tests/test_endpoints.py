import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.routes import router as books_router


client = TestClient(app)

def test_get_all_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert "books" in response.json()

def test_add_book():
    payload = {
    "title":  "tst",
    "author": "levan lomidze",
    "price": 19.25
    }
    response = client.post("/books", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["message"] == "Book added"
    assert json_data["book"]["title"] == 'tst'
    return json_data["book"]["id"]

    # this function tests if the filtering endpoint filters well
def test_filter_books():
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "price": 15.99
    }
    create = client.post("/books", json=book_data)
    assert create.status_code == 201
    response = client.get ("/books/filter", params = {"title": "1984"})
    assert response.status_code == 200
    books = response.json()
    assert isinstance(response.json(), list)
    assert len(books) > 0
    found = any(book["title"].lower() == "1984" for book in books)
    assert found, "Expected book with the title '1984' not found in the DB"

def test_update_book():
    payload = {
    "title":  "tst11",
    "author": "levan update",
    "price": 69.96
    }
    create = client.post("/books", json=payload)
    book_id = create.json()["book"]["id"]

    updated = {
    "title":  "updated",
    "author": "michael update",
    "price": 34.68
    }
    print("CREATE:", create.status_code, create.json())
    response = client.patch(f"/books/{book_id}", json=updated)
    assert response.status_code == 200
    assert response.json()["book"]["title"] == "updated"

def test_delete_book():
    book = {
        "title": "Delete Me",
        "author": "Someone",
        "price": 5.0}
    create = client.post("/books", json = book)
    book_id = create.json()["book"]["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["book"]["id"] == book_id
