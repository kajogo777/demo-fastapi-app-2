from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, Boolean, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ADDRESS = os.getenv("DB_ADDRESS")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_ADDRESS, DB_NAME]):
    raise Exception(
        "Missing required environment variables. Please ensure DB_USER, DB_PASSWORD, DB_ADDRESS and DB_NAME are set."
    )

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}"


# Wait for database to be ready
while True:
    try:
        conn = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
        conn.close()
        break
    except psycopg2.OperationalError as e:
        print(f"Database not ready. Waiting for {DB_ADDRESS}...\n{e}")
        time.sleep(1)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
