from models import Book
from db import SessionLocal
from sqlalchemy.orm import Session
def insert_data(filepath: str):
    db: Session = SessionLocal
    try:
        count = db.query(Book).count()
        if count > 0:
            print("Books table already initialized.")
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            title, author, price_str = [x.strip() for x in line.strip().split(',')]
            price = float(price_str)

            book = Book(title=title, author=author, price=price)
            db.add(book)
        db.commit()
        print(f"{len(lines)} books inserted successfully.")
    finally:
        db.close()

