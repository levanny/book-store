from fastapi import APIRouter, HTTPException, status, Depends
from models import Book
from db import get_db
from typing import Optional
from sqlalchemy.orm import sessionmaker, Session


router = APIRouter()

# Get all books
@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return {"books": [{"id": b.id, "title": b.title, "author": b.author, "price": b.price} for b in books]}


# Get books by filter
@router.get("/books/filter")
def get_book_by_filter(
        id: Optional[int] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        price: Optional[float] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        db: Session = Depends(get_db)
):
    query = db.query(Book)

    if id is not None:
        query = query.filter(Book.id == id)
    if title is not None:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author is not None:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if price is not None:
        query = query.filter(Book.price == price)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)

    results = query.all()
    if not results:
        raise HTTPException(status_code=404, detail="No books found")

    return [{"id": b.id, "title": b.title, "author": b.author, "price": b.price} for b in results]


# Add a book
@router.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: Book, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author, price=book.price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {"message": "Book added", "book": {"id": db_book.id, "title": db_book.title, "author": db_book.author, "price": db_book.price}}


# Update a book
@router.patch("/books/{book_id}")
def update_book(book_id: int, updated_book: Book, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    book.price = updated_book.price
    db.commit()
    db.refresh(book)

    return {"message": "Book updated",
            "book": {"id": book.id, "title": book.title, "author": book.author, "price": book.price}}


# Delete a book
@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted", "book": {"id": book.id}}