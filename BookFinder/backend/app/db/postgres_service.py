import os
from typing import List, Optional
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from schemas.rating_schema import RatingResponse

# Import your models
from db.models import (
    Book,
    BookStoreInventory,
    BookSimilarity,
    SearchQuery,
    Ratings,
    Bookstore,
    AppUser
)

# -------------------------
# Book methods
# -------------------------

def get_book_by_id(db: Session, book_id: int) -> Optional[Book]:
    """
    Retrieve a book by its ID.

    Args:
        db (Session): SQLAlchemy session.
        book_id (int): ID of the desired book.

    Returns:
        Optional[Book]: The book if found, otherwise None.
    """
    return db.query(Book).filter(Book.book_id == book_id).first()


def search_books_by_title(db: Session, search_term: str, limit: int = 20) -> List[Book]:
    """
    Search for books by partial title match.

    Args:
        db (Session): SQLAlchemy session.
        search_term (str): Text to search for in book titles.
        limit (int): Maximum number of results to return.

    Returns:
        List[Book]: List of matching books.
    """
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).limit(limit).all()


def insert_book(
    db: Session,
    title: str,
    author: str,
    genre: str,
    description: str,
    isbn: str,
    source: str = "local"
) -> int:
    """
    Insert a new book into the database.

    Args:
        db (Session): SQLAlchemy session.
        title (str): Title of the book.
        author (str): Author name.
        genre (str): Genre of the book.
        description (str): Book description.
        isbn (str): ISBN identifier.
        source (str): Data source flag.

    Returns:
        int: ID of the newly created book.
    """
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
    """
    Fetch all books from the database.

    Args:
        db (Session): SQLAlchemy session.

    Returns:
        List[Book]: All books in the database.
    """
    return db.query(Book).all()


# -------------------------
# Bookstore / Inventory
# -------------------------

def get_stores_for_book(db: Session, book_id: int) -> List[BookStoreInventory]:
    """
    Retrieve all store inventory entries for a given book.

    Args:
        db (Session): SQLAlchemy session.
        book_id (int): Book identifier.

    Returns:
        List[BookStoreInventory]: List of store entries ordered by price.
    """
    return (
        db.query(BookStoreInventory)
        .join(Bookstore)
        .filter(BookStoreInventory.book_id == book_id)
        .order_by(BookStoreInventory.price.asc())
        .all()
    )


def insert_inventory_entry(db: Session, book_id: int, store_id: int, price: float) -> BookStoreInventory:
    """
    Insert or update an inventory entry for a book in a store.

    Args:
        db (Session): SQLAlchemy session.
        book_id (int): Book ID.
        store_id (int): Store ID.
        price (float): Book price in this store.

    Returns:
        BookStoreInventory: The created or updated inventory entry.
    """
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
# Search logging
# -------------------------

def log_search_query(db: Session, user_id: int = None, term: str = "", matched_book_id: int = None) -> SearchQuery:
    """
    Log a user search query for analytics and tracking.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int, optional): ID of the user who performed the search.
        term (str): Search term.
        matched_book_id (int, optional): ID of the book that matched the query.

    Returns:
        SearchQuery: The logged query record.
    """
    entry = SearchQuery(user_id=user_id, search_term=term, matched_book_id=matched_book_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_searches(db: Session, limit: int = 20) -> List[SearchQuery]:
    """
    Retrieve the most recent search queries.

    Args:
        db (Session): SQLAlchemy session.
        limit (int): Maximum number of results.

    Returns:
        List[SearchQuery]: Recent search logs.
    """
    return (
        db.query(SearchQuery)
        .order_by(SearchQuery.query_id.desc())
        .limit(limit)
        .all()
    )


# -------------------------
# Ratings
# -------------------------

def add_or_update_rating(db: Session, user_id: int, book_id: int, rating_value: int, comment: str = None) -> Ratings:
    """
    Create or update a rating for a book by a specific user.

    Args:
        db (Session): SQLAlchemy session.
        user_id (int): ID of the user rating the book.
        book_id (int): ID of the book being rated.
        rating_value (int): Rating score.
        comment (str, optional): Optional written feedback.

    Returns:
        Ratings: The created or updated rating record.
    """
    existing_rating = db.query(Ratings).filter_by(user_id=user_id, book_id=book_id).first()

    if existing_rating:
        existing_rating.rating = rating_value
        existing_rating.comment = comment
        db.commit()
        db.refresh(existing_rating)
        return existing_rating

    new_rating = Ratings(user_id=user_id, book_id=book_id, rating=rating_value, comment=comment)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


def get_ratings_for_book(db: Session, book_id: int) -> List[RatingResponse]:
    """
    Retrieve ratings for a given book and convert them into response schemas.

    Args:
        db (Session): SQLAlchemy session.
        book_id (int): ID of the book.

    Returns:
        List[RatingResponse]: List of rating response models.
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
