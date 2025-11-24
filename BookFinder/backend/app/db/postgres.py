import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# -------------------------
# Load environment variables
# -------------------------
load_dotenv(".env")
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# -------------------------
# SQLAlchemy setup
# -------------------------
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------
# Session helper
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()