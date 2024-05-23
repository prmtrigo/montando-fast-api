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

def test_remove_book_by_id():
    response = client.post("/add-book", json={
        "title": "Sample Book",
        "author": "Author Name",
        "genre": "fiction",
        "price": 19.99
    })
    assert response.status_code == 200
    book_id = BOOK_DATABASE[0]["book_id"]
    response = client.delete(f"/remove-book-by-id/{book_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Book was removed from the Bookstore"}
    assert len(BOOK_DATABASE) == 0

    # Testa a remoção de um ID inexistente
    response = client.delete(f"/remove-book-by-id/{book_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book_title():
    response = client.post("/add-book", json={
        "title": "Sample Book",
        "author": "Author Name",
        "genre": "fiction",
        "price": 19.99
    })
    assert response.status_code == 200
    book_id = BOOK_DATABASE[0]["book_id"]

    new_title = "Updated Book Title"
    response = client.put(f"/update-book-title/{book_id}", params={"title": new_title})
    assert response.status_code == 200
    assert response.json() == {"message": "Book was updated"}
    assert BOOK_DATABASE[0]["title"] == new_title

    response = client.put("/update-book-title/nonexistent_id", params={"title": new_title})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_update_book_price():
    response = client.post("/add-book", json={
        "title": "Sample Book",
        "author": "Author Name",
        "genre": "fiction",
        "price": 19.99
    })
    assert response.status_code == 200
    book_id = BOOK_DATABASE[0]["book_id"]

    new_price = 29.99
    response = client.put(f"/update_book_price/{book_id}", params={"price": new_price})
    assert response.status_code == 200
    assert response.json() == {"message": "Book was updated"}
    assert BOOK_DATABASE[0]["price"] == new_price

    response = client.put("/update_book_price/nonexistent_id", params={"price": new_price})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_list_book_by_genre():
    response = client.post("/add-book", json={
        "title": "Fiction Book",
        "author": "Author One",
        "genre": "fiction",
        "price": 19.99
    })
    assert response.status_code == 200

    response = client.post("/add-book", json={
        "title": "Non-Fiction Book",
        "author": "Author Two",
        "genre": "non-fiction",
        "price": 29.99
    })
    assert response.status_code == 200

    response = client.get("/list-book-by-genre/fiction")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 1
    assert response.json()["books"][0]["title"] == "Fiction Book"

    response = client.get("/list-book-by-genre/non-fiction")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 1
    assert response.json()["books"][0]["title"] == "Non-Fiction Book"

    response = client.get("/list-book-by-genre/science")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 0

def test_random_book_no_books():
    response = client.get("/random-book")
    assert response.status_code == 404
    assert response.json() == {"detail": "No books available"}

def test_random_book_with_books():
    book1 = {
        "title": "Sample Book 1",
        "author": "Author One",
        "genre": "fiction",
        "price": 19.99
    }
    book2 = {
        "title": "Sample Book 2",
        "author": "Author Two",
        "genre": "non-fiction",
        "price": 29.99
    }
    
    response = client.post("/add-book", json=book1)
    assert response.status_code == 200
    response = client.post("/add-book", json=book2)
    assert response.status_code == 200

    response = client.get("/random-book")
    assert response.status_code == 200
    assert "book" in response.json()
    book = response.json()["book"]
    assert book in BOOK_DATABASE

def test_list_book_by_author():
    book1 = {
        "title": "Sample Book 1",
        "author": "Author One",
        "genre": "fiction",
        "price": 19.99
    }
    book2 = {
        "title": "Sample Book 2",
        "author": "Author Two",
        "genre": "non-fiction",
        "price": 29.99
    }
    book3 = {
        "title": "Sample Book 3",
        "author": "Author One",
        "genre": "fiction",
        "price": 15.99
    }

    response = client.post("/add-book", json=book1)
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}

    response = client.post("/add-book", json=book2)
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}

    response = client.post("/add-book", json=book3)
    assert response.status_code == 200
    assert response.json() == {"message": "New Book was added to the Bookstore"}

    response = client.get("/list-book-by-author?author=Author One")
    assert response.status_code == 200
    books_by_author_one = response.json()["books"]
    assert len(books_by_author_one) == 2
    assert books_by_author_one[0]["title"] == "Sample Book 1"
    assert books_by_author_one[1]["title"] == "Sample Book 3"

    response = client.get("/list-book-by-author?author=Author Two")
    assert response.status_code == 200
    books_by_author_two = response.json()["books"]
    assert len(books_by_author_two) == 1
    assert books_by_author_two[0]["title"] == "Sample Book 2"

    response = client.get("/list-book-by-author?author=Author Three")
    assert response.status_code == 200
    assert len(response.json()["books"]) == 0
