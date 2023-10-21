from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID


app = FastAPI()


class Book(BaseModel):
    uuid: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = []


@app.get("/")
def read_api():
    return BOOKS


@app.post("/")
def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.put("/{book_id}")
def update_book(book_id: UUID, book: Book):
    ctr = 0

    for x in BOOKS:
        if x.uuid == book_id:
            BOOKS[ctr] = book
            return BOOKS[ctr]
        ctr += 1

    raise HTTPException(
        status_code=404,
        detail=f"ID: {book_id} does not exist"
    )


@app.delete("/{book_id}")
def delete_book(book_id: UUID):
    ctr = 0

    for x in BOOKS:
        if x.uuid == book_id:
            del BOOKS[ctr]
            return f"ID: {book_id} has been deleted"
        ctr += 1
    raise HTTPException(
        status_code=404,
        detail=f"ID: {book_id} does not exists!"
    )
