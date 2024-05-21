import pytest
from fastapi.testclient import TestClient
from main import app, BOOK_DATABASE

client = TestClient(app)

# Helper function to reset the BOOK_DATABASE before each test
@pytest.fixture(autouse=True)
def reset_database():
    global BOOK_DATABASE
    BOOK_DATABASE.clear()

def test_find_book():
    response = client.post("/add-book", json={
        "title": "Sample Book",
        "author": "Author Name",
        "genre": "fiction",
        "price": 19.99
    })
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}

    book_id = BOOK_DATABASE[0]["book_id"]

    response = client.get(f"/find-book/{book_id}")
    assert response.status_code == 200
    assert response.json()["book"]["title"] == "Sample Book"
    assert response.json()["book"]["author"] == "Author Name"
    assert response.json()["book"]["genre"] == "fiction"
    assert response.json()["book"]["price"] == 19.99

    response = client.get("/find-book/nonexistent_id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_add_book():
    response = client.post("/add-book", json={
        "title": "Sample Book",
        "author": "Author Name",
        "genre": "fiction",
        "price": 19.99
        })
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}
    assert len(BOOK_DATABASE) == 1
    assert BOOK_DATABASE[0]["title"] == "Sample Book"
    assert BOOK_DATABASE[0]["author"] == "Author Name"
    assert BOOK_DATABASE[0]["genre"] == "fiction"
    assert BOOK_DATABASE[0]["price"] == 19.99

    response = client.post("/add-book", json={
        "title": "Another Book",
        "author": "Another Name",
        "genre": "non-fiction",
        "price": 29.99
        })
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}
    assert len(BOOK_DATABASE) == 2
    assert BOOK_DATABASE[1]["title"] == "Another Book"
    assert BOOK_DATABASE[1]["author"] == "Another Name"
    assert BOOK_DATABASE[1]["genre"] == "non-fiction"
    assert BOOK_DATABASE[1]["price"] == 29.99

