from db import get_connection
from models import Book

def insert_data(filepath: str):
    with get_connection() as con:
        with con.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM books")
            count = cur.fetchone()[0]

            if count > 0:
                print("Books table already initialized.")
                return

            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                title, author, price_str = [x.strip() for x in line.strip().split(',')]
                price = float(price_str)
                book = Book(id=None, title=title, author=author, price=price)
                cur.execute(
                    "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)",
                    (book.title, book.author, book.price)
                )

        con.commit()
        print(f'{len(lines)} books inserted successfully.')




