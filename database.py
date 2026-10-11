import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase



load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError("Database Connection is not configured")


# Setup engine

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Setup session

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False

)

# Setup one session per request

def get_db():
    db = SessionLocal()
    try:
        yield db;
    finally:
        db.close()



# Base class for sqlalchemy model
class Base(DeclarativeBase):
    pass