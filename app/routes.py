from fastapi import APIRouter, HTTPException, status
from app.models import Book
from app.db import get_connection
from typing import Optional

router = APIRouter()

#This endpoint is responsible for just accessing a single book by just its id.
@router.get("/books/filter")
def get_book_by_filter(
    id: Optional[int] = None,
    title: Optional[str] = None,
    author: Optional[str] = None,
    price: Optional[float] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = "SELECT id, title, author, price FROM books WHERE TRUE"
    params = []

    if id:
        query += " AND id = %s"
        params.append(id)
    if title:
        query += " AND LOWER(title) LIKE %s"
        params.append(f"%{title.lower()}%")
    if author:
        query += " AND LOWER(author) LIKE %s"
        params.append(f"%{author.lower()}%")
    if price:
        query += " AND price = %s"
        params.append(price)
    if min_price:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    with get_connection() as con:
        with con.cursor() as cur:           # DO NOT FORGET TO INCLUDE MAX_PRICE AND MIN_PRICE ! ! ! ! ! !
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail="No books found")
            return [
                {"id": row[0], "title": row[1], "author": row[2], "price": row[3]}
                for row in rows
            ]

#This endpoint is responsible for adding a book to the table, by inputting { title, author, price }, { id } is PRIMARY, so it is being generated on itself
@router.post("/books", status_code=status.HTTP_201_CREATED)
def add_book(book: Book):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute(
                "INSERT INTO books (title, author, price) VALUES (%s, %s, %s) RETURNING *",
                (book.title, book.author, book.price),
            )
            row = cur.fetchone()
            con.commit()
            return {"message": "Book added", "book": {"id": row[0], "title": row[1], "author": row[2], "price": row[3]}}

# This endpoint is responsible for deleting a book by accessing it by its { id }
@router.delete("/books/{book_id}")
def delete_book(book_id: int):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            con.commit()
            return {"message": "Book deleted", "book": {"id": result[0]}}

# This endpoint is responsible for updating an already existing book by accessing it by its { id }
@router.patch("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT 1 FROM books WHERE id = %s", (book_id,))
            if not cur.fetchone():
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
            cur.execute("""
                UPDATE books SET title = %s, author = %s, price = %s WHERE id = %s
            """, (updated_book.title, updated_book.author, updated_book.price, book_id))
            con.commit()
            return {"message": "Book updated", "book": {"id": book_id, **updated_book.dict()}}

# This endpoint is responsible for printing the whole table
@router.get("/books")
def get_books():
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT id, title, author, price FROM books")  # Select everything from the table
            rows = cur.fetchall()
            books = []
            for row in rows:
                books.append({"id": row[0], "title": row[1], "author": row[2], "price": row[3]})
            return {"books": books}
