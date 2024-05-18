import json
import os
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    genre: Literal["fiction", "non-fiction"]
    price: float
    book_id: Optional[str] = uuid4().hex

BOOK_DATABASE = []

BOOKS_FILE = "books.json"

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

# / -> home
@app.get("/")
async def home():
    return "Hello, this is my bookstore"

# /list-books -> list books
@app.get("/list-books")
async def list_books():
    return {"books": BOOK_DATABASE}

# /find-book/{book_id} -> find book by id
@app.get("/find-book/{book_id}")
async def find_book(book_id: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return {"book": book}
    raise HTTPException(404, "Book not found")

# /random-book -> random book
@app.get("/random-book")
async def random_book():
    if not BOOK_DATABASE:
        raise HTTPException(404, "No books available")
    return {"book": random.choice(BOOK_DATABASE)}

# /add-book -> add new book
@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f, indent=4)
    return {"message": "New Book was added to the Bookstore"}

# /remove-book-by-id -> remove book by id
@app.delete("/remove-book-by-id/{book_id}")
async def remove_book_by_id(book_id: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            BOOK_DATABASE.remove(book)
            with open(BOOKS_FILE, "w") as f:
                json.dump(BOOK_DATABASE, f, indent=4)
            return {"message": "Book was removed from the Bookstore"}
    raise HTTPException(404, "Book not found")

# /remove-book-by-title -> remove book by title
@app.delete("/remove-book-by-title/{title}")
async def remove_book_by_title(title: str):
    for book in BOOK_DATABASE:
        if book["title"].lower() == title.lower():
            BOOK_DATABASE.remove(book)
            with open(BOOKS_FILE, "w") as f:
                json.dump(BOOK_DATABASE, f, indent=4)
            return {"message": "Book was removed from the Bookstore"}
    raise HTTPException(404, "Book not found")

#/update-book-title/{book_id} -> update book title
@app.put("/update-book-title/{book_id}")
async def update_book_title(book_id: str, title: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            book["title"] = title
            with open(BOOKS_FILE, "w") as f:
                json.dump(BOOK_DATABASE, f, indent=4)
                return {"message": "Book was updated"}
    raise HTTPException(404, "Book not found")

#/update-book-price/{book_id} -> update book price
@app.put("/update_book_price/{book_id}")
async def update_book_price(book_id: str, price: float):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            book["price"] = price
            with open(BOOKS_FILE, "w") as f:
                json.dump(BOOK_DATABASE, f, indent=4)
                return {"message": "Book was updated"}
    raise HTTPException(404, "Book not found")
