from db import get_connection
from app.models import Book

def insert_data(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with get_connection() as con:
        with con.cursor() as cur:
            for line in lines:
                title, author, price_str = line.strip().split(',')
                price = float(price_str)
                book = Book(id= None, title = title, author = author, price = price)
                cur.execute("""
                INSERT INTO books (title, author, price) VALUES (%s, %s, %s)     
                """,
                (book.title, book.author, book.price)
                )
        con.commit()
    print('Books inserted successfully')

