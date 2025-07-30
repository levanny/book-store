import psycopg
from psycopg.errors import DuplicateTable

DB_NAME = "book_store"

DB_CONFIG = {
    "dbname": DB_NAME,
    "user": "postgres",
    "password": "FantasticFox",
    "host": "localhost",
    "port": "5432",

}

ADMIN_DB_CONFIG = DB_CONFIG.copy()
ADMIN_DB_CONFIG["dbname"] = "postgres"

def ensure_db_exists():
    try:
        with psycopg.connect(**ADMIN_DB_CONFIG, autocommit= True) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
                exists = cur.fetchone()
                if not exists:
                    cur.execute(f"CREATE DATABASE {DB_NAME};")
                    print(f"Database '{DB_NAME}' created.")
                else:
                    print(f"Database '{DB_NAME}' already exists.")
    except Exception as e:
        print(f"Database creation failed - {e}")


def get_connection():
    return psycopg.connect(**DB_CONFIG)

def create_books_table():
    ensure_db_exists()
    with get_connection() as con:
        with con.cursor() as cur:
            try:
                cur.execute("""
                    CREATE TABLE books (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        author TEXT NOT NULL,
                        price FLOAT NOT NULL
                    )
                """)
                print("Table created successfully")
            except DuplicateTable:
                print("Table already exists")

