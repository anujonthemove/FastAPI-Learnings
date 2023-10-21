from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# when this is run, this is going to create the database
# and table if it does not already exists
# and then we can connect all our CRUD operations to now
# use the db we are creating
models.Base.metadata.create_all(bind=engine)


# singleton?
def get_db():
    try:
        # this creates a
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()


@app.post("/")
def create_book(book: Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.put("/{book_id}")
def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    # guard clause
    if book_model is None:
        raise HTTPException(status_code=404, detail=f"ID: {book_id} does not exist")
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book


@app.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(status_code=404, detail=f"ID: {book_id} does not exists!")
    db.query(models.Books).filter(models.Books.id == book_id).delete()
    db.commit()
