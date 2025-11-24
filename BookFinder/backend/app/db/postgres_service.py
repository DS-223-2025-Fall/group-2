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
def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.book_id == book_id).first()


def search_books_by_title(db: Session, search_term: str, limit: int = 20) -> List[Book]:
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).limit(limit).all()


def insert_book(db: Session, title: str, author: str, genre: str, description: str, isbn: str, source: str = "local") -> int:
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
    return new_book.book_id

    
def get_allBooks(db: Session) -> List[Ratings]:
    return db.query(Book).all()

# -------------------------
# Bookstore / Inventory
# -------------------------
def get_stores_for_book(db: Session, book_id: int) -> List[BookStoreInventory]:
    return db.query(BookStoreInventory).join(Bookstore).filter(
        BookStoreInventory.book_id == book_id
    ).order_by(BookStoreInventory.price.asc()).all()


def insert_inventory_entry(db: Session, book_id: int, store_id: int, price: float) -> BookStoreInventory:
    entry = db.query(BookStoreInventory).filter_by(book_id=book_id, store_id=store_id).first()
    if entry:
        entry.price = price
    else:
        entry = BookStoreInventory(book_id=book_id, store_id=store_id, price=price)
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# -------------------------
# Similarity methods
# -------------------------
def get_similar_books(db: Session, book_id: int, top_n: int = 10) -> List[BookSimilarity]:
    return db.query(BookSimilarity).join(Book, Book.book_id == BookSimilarity.book_id_2)\
        .filter(BookSimilarity.book_id_1 == book_id)\
        .order_by(BookSimilarity.similarity_score.desc())\
        .limit(top_n).all()


def insert_similarity(db: Session, book1: int, book2: int, score: float) -> BookSimilarity:
    entry = db.query(BookSimilarity).filter_by(book_id_1=book1, book_id_2=book2).first()
    if entry:
        entry.similarity_score = score
    else:
        entry = BookSimilarity(book_id_1=book1, book_id_2=book2, similarity_score=score)
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# -------------------------
# Search logging
# -------------------------
def log_search_query(db: Session, user_id: int = None, term: str = "", matched_book_id: int = None) -> SearchQuery:
    entry = SearchQuery(user_id=user_id, search_term=term, matched_book_id=matched_book_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_searches(db: Session, limit: int = 20) -> List[SearchQuery]:
    return db.query(SearchQuery).order_by(SearchQuery.query_id.desc()).limit(limit).all()

# -------------------------
# Ratings
# -------------------------
def add_or_update_rating(db: Session, user_id: int, book_id: int, rating_value: int, comment: str = None) -> Ratings:
    existing_rating = db.query(Ratings).filter_by(user_id=user_id, book_id=book_id).first()
    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.comment = comment
        db.commit()
        db.refresh(existing_rating)
        return existing_rating
    else:
        new_rating = Ratings(user_id=user_id, book_id=book_id, rating=rating_value, comment=comment)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating

def get_ratings_for_book(db: Session, book_id: int) -> List[RatingResponse]:
    """
    Fetch all ratings for a given book_id from the database
    and return them as a list of RatingResponse.
    """
    ratings = db.query(Ratings).filter(Ratings.book_id == book_id).all()
    return [
        RatingResponse(
            bookId=str(r.book_id),
            user_email=r.user.email,
            rating=r.rating,
            comment=r.comment
        )
        for r in ratings
    ]
