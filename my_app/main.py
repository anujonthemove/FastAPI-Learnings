from fastapi import FastAPI, HTTPException
from datetime import datetime
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from uuid import uuid4
from fastapi.encoders import jsonable_encoder


app = FastAPI()


# Book Model
class Book(BaseModel):
    name: str
    price: float
    genere: Literal["fiction", "non-fiction"]
    book_id: Optional[str] = uuid4().hex


BOOKS_FILE = "books.json"
BOOK_DB = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DB = json.load(f)


@app.get("/")
async def home():
    return {"message": "Hello, welcome to my Book Store!"}


@app.get("/get-current-time")
async def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return {"message": f"Time is: {current_time}"}


@app.get("/list-books")
async def list_books():
    return {"book": BOOK_DB}


@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
    if index < 0 or index >= len(BOOK_DB):
        raise HTTPException(404, f"Index {index} is out of range: {len(BOOK_DB)}")
    return {"book": BOOK_DB[index]}


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DB.append(json_book)
    with open(BOOKS_FILE, "w+") as f:
        json.dump(BOOK_DB, f)

    return {"message": f"Book {book} has been added", "book_id": book.book_id}
