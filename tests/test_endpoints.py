import pytest
from fastapi.testclient import TestClient
from app.main import app

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
    # def test_filter_books():