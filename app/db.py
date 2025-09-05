from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()



DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

DB_NAME = DATABASE_URL.rsplit("/", 1)[-1]
ADMIN_DB_CONFIG = {
    "dbname": "postgres",
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "FantasticFox"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
}


def ensure_db_exists():
    try:
        with psycopg.connect(**ADMIN_DB_CONFIG, autocommit=True) as conn:
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

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

