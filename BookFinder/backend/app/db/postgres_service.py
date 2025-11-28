import os
from typing import List, Optional
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from schemas.rating_schema import RatingResponse

# Import your models
from db.models import Book, BookStoreInventory, BookSimilarity, SearchQuery, Ratings, Bookstore, AppUser

# Book methods
# -------------------------

def get_book_by_isbn(db: Session, isbn: str) -> Optional[Book]:
    """Get book by ISBN"""
    return db.query(Book).filter(Book.ISBN == isbn).first()


def search_books_by_title(db: Session, search_term: str, limit: int = 20) -> List[Book]:
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).limit(limit).all()


def insert_book(db: Session, title: str, author: str, genre: str, description: str, isbn: str, source: str = "local") -> str:
    new_book = Book(
        title=title,
        author=author,
        genre=genre,
        description=description,
        ISBN=isbn,
        data_source=source
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book.ISBN

    
def get_allBooks(db: Session) -> List[Ratings]:
    return db.query(Book).all()

# -------------------------
# Bookstore / Inventory
# -------------------------
def get_stores_for_book(db: Session, isbn: str) -> List[BookStoreInventory]:
    return db.query(BookStoreInventory).join(Bookstore).filter(
        BookStoreInventory.ISBN == isbn
    ).order_by(BookStoreInventory.price.asc()).all()


def insert_inventory_entry(db: Session, isbn: str, store_id: int, price: float) -> BookStoreInventory:
    entry = db.query(BookStoreInventory).filter_by(ISBN=isbn, store_id=store_id).first()
    if entry:
        entry.price = price
    else:
        entry = BookStoreInventory(ISBN=isbn, store_id=store_id, price=price)
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# -------------------------
# Similarity methods
# -------------------------
def get_similar_books(db: Session, isbn: str, top_n: int = 10) -> List[BookSimilarity]:
    return db.query(BookSimilarity).join(Book, Book.ISBN == BookSimilarity.ISBN_2)\
        .filter(BookSimilarity.ISBN_1 == isbn)\
        .order_by(BookSimilarity.similarity_score.desc())\
        .limit(top_n).all()


def insert_similarity(db: Session, isbn1: str, isbn2: str, score: float) -> BookSimilarity:
    entry = db.query(BookSimilarity).filter_by(ISBN_1=isbn1, ISBN_2=isbn2).first()
    if entry:
        entry.similarity_score = score
    else:
        entry = BookSimilarity(ISBN_1=isbn1, ISBN_2=isbn2, similarity_score=score)
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# -------------------------
# Search logging
# -------------------------
def log_search_query(db: Session, user_id: int = None, term: str = "", matched_book_isbn: str = None) -> SearchQuery:
    entry = SearchQuery(user_id=user_id, search_term=term, matched_book_ISBN=matched_book_isbn)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_searches(db: Session, limit: int = 20) -> List[SearchQuery]:
    return db.query(SearchQuery).order_by(SearchQuery.query_id.desc()).limit(limit).all()

# -------------------------
# Ratings
# -------------------------
def add_or_update_rating(db: Session, user_id: int, isbn: str, rating_value: int, comment: str = None) -> Ratings:
    existing_rating = db.query(Ratings).filter_by(user_id=user_id, ISBN=isbn).first()
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.comment = comment
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        new_rating = Ratings(user_id=user_id, ISBN=isbn, rating=rating_value, comment=comment)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating

def get_ratings_for_book(db: Session, isbn: str) -> List[RatingResponse]:
    """
    Fetch all ratings for a given ISBN from the database
    and return them as a list of RatingResponse.
    """
    ratings = db.query(Ratings).filter(Ratings.ISBN == isbn).all()
    return [
        RatingResponse(
            bookId=str(r.ISBN),
            user_email=r.user.email,
            rating=r.rating,
            comment=r.comment
        )
        for r in ratings
    ]
