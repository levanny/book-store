from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()



class Book(BaseModel):
    name: str
    price: float


books = [
    {"id": 1, "name": "1984", "price": 100},
    {"id": 2, "name": "Bible", "price": 200},
]
next_id = 3

@app.get("/books")
def get_books():
    return books

@app.post("/books")
def add_book(book: Book):
    global next_id
    new_book = {
        "id": next_id,
        "name": book.name,
        "price": book.price
                }
    next_id += 1
    books.append(new_book)
 #   return {"message": "New book added", "book": new_book}
    raise HTTPException(status_code=201, detail="successfully added new book")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    global next_id
    for i, book in enumerate(books):
        if book["id"] == book_id:
            deleted_book = books.pop(i)
            return {"message": "Book deleted", "book": deleted_book}
    raise HTTPException(status_code = 404, detail = "Book not found")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code = 404, detail = "Book not found")

@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: Book):
    for book in books:
        if book["id"] == book_id:
            book["name"] = updated_book.name
            book["price"] = updated_book.price
            return {"message ": "Book updated", "book": book}
    raise HTTPException(status_code = 404, detail = "Book not found")