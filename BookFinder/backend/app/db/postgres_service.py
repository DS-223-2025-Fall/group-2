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
    """Get a book object from the database by its ISBN.
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn (str): ISBN of the book to retrieve.
        
    Returns:
        Optional[Book]: Book object if found, otherwise None.
    """
    return db.query(Book).filter(Book.ISBN == isbn).first()


def search_books_by_title(db: Session, search_term: str, limit: int = 20) -> List[Book]:
    """Search for books whose title contains the given search term.
    
    Args:
        db (Session): SQLAlchemy database session.
        search_term (str): Term to search in book titles.
        limit (int, optional): Maximum number of results. Defaults to 20.
        
    Returns:
        List[Book]: List of Book objects matching the search term.
    """
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).limit(limit).all()


def insert_book(db: Session, title: str, author: str, genre: str, description: str, isbn: str, source: str = "local") -> str:
    """Insert a new book into the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        title (str): Book title.
        author (str): Book author.
        genre (str): Book genre.
        description (str): Book description.
        isbn (str): Book ISBN.
        source (str, optional): Source of the book data. Defaults to "local".
        
    Returns:
        str: ISBN of the newly inserted book.
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
    return new_book.ISBN

    
def get_allBooks(db: Session) -> List[Ratings]:
    """Retrieve all books from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        
    Returns:
        List[Ratings]: List of all Book objects.
    """
    return db.query(Book).all()

# -------------------------
# Bookstore / Inventory
# -------------------------
def get_stores_for_book(db: Session, isbn: str) -> List[BookStoreInventory]:
    """Get all bookstores that have the book in inventory, ordered by price ascending.
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn (str): ISBN of the book.
        
    Returns:
        List[BookStoreInventory]: List of inventory entries for the book.
    """
    return db.query(BookStoreInventory).join(Bookstore).filter(
        BookStoreInventory.ISBN == isbn
    ).order_by(BookStoreInventory.price.asc()).all()


def insert_inventory_entry(db: Session, isbn: str, store_id: int, price: float) -> BookStoreInventory:
    """Insert or update an inventory entry for a book in a bookstore.
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn (str): ISBN of the book.
        store_id (int): ID of the bookstore.
        price (float): Price of the book.
        
    Returns:
        BookStoreInventory: The created or updated inventory entry.
    """
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
    """Retrieve the most similar books to a given book by ISBN.
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn (str): ISBN of the reference book.
        top_n (int, optional): Number of similar books to return. Defaults to 10.
        
    Returns:
        List[BookSimilarity]: List of BookSimilarity objects ordered by similarity score descending.
    """
    return db.query(BookSimilarity).join(Book, Book.ISBN == BookSimilarity.ISBN_2)\
        .filter(BookSimilarity.ISBN_1 == isbn)\
        .order_by(BookSimilarity.similarity_score.desc())\
        .limit(top_n).all()


def insert_similarity(db: Session, isbn1: str, isbn2: str, score: float) -> BookSimilarity:
    """Insert or update a similarity score between two books.
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn1 (str): ISBN of the first book.
        isbn2 (str): ISBN of the second book.
        score (float): Similarity score between the two books.
        
    Returns:
        BookSimilarity: The created or updated similarity entry.
    """
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
    """Log a user's search query in the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_id (int, optional): ID of the user performing the search. Defaults to None.
        term (str, optional): Search term used. Defaults to "".
        matched_book_isbn (str, optional): ISBN of matched book if any. Defaults to None.
        
    Returns:
        SearchQuery: The created search query entry.
    """
    entry = SearchQuery(user_id=user_id, search_term=term, matched_book_ISBN=matched_book_isbn)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_recent_searches(db: Session, limit: int = 20) -> List[SearchQuery]:
    """Retrieve the most recent search queries from the database.
    
    Args:
        db (Session): SQLAlchemy database session.
        limit (int, optional): Number of recent searches to retrieve. Defaults to 20.
        
    Returns:
        List[SearchQuery]: List of recent search queries ordered by most recent first.
    """
    return db.query(SearchQuery).order_by(SearchQuery.query_id.desc()).limit(limit).all()

# -------------------------
# Ratings
# -------------------------
def add_or_update_rating(db: Session, user_id: int, isbn: str, rating_value: int, comment: str = None) -> Ratings:
    """Add a new rating or update an existing rating for a book by a user.
    
    Args:
        db (Session): SQLAlchemy database session.
        user_id (int): ID of the user providing the rating.
        isbn (str): ISBN of the book being rated.
        rating_value (int): Rating value.
        comment (str, optional): Optional comment for the rating. Defaults to None.
        
    Returns:
        Ratings: The created or updated Ratings object.
    """
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
    
    Args:
        db (Session): SQLAlchemy database session.
        isbn (str): ISBN of the book for which to fetch ratings.
    
    Returns:
        List[RatingResponse]: List of ratings with user email, rating value, and comment.
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
