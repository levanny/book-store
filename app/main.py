from fastapi import FastAPI
from app.routes import router as books_router
import uvicorn
from app.db import ensure_db_exists, create_books_table
from app.init_db import insert_data

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Biblusi!"}

@app.on_event("startup")
def startup():
    ensure_db_exists()
    create_books_table()
    insert_data('books_data.txt')

app.include_router(books_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

