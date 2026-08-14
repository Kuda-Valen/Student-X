# Database connection & session factory
import os 
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connectoiin string (Reads from environment variable or default to local)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgre@localhost:5432/tracker_db"
)

# Initialize SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session local factory for request-scoped database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative ORM models
Base = declarative_base()

def get_db():
    """Dependency that yields a database session per request and close it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()