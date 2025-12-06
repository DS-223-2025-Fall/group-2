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
    """
    **Retrieve a book from the database using its ISBN.**

    This function queries the database for a book matching the provided ISBN.  
    If a match exists, the corresponding **Book** object is returned; otherwise, the function returns **None**.

    Returns:
        Optional[Book]: Book object if found, otherwise None.
    """
    return db.query(Book).filter(Book.ISBN == isbn).first()


def search_books_by_title(db: Session, search_term: str, limit: int = 20) -> List[Book]:
    """
    **Search for books based on a partial title match.**

    This function performs a case-insensitive lookup and returns all books whose
    titles **contain** the provided search term.  
    You can optionally limit the maximum number of returned results.

    Args:
        db (Session): SQLAlchemy database session.
        search_term (str): Term to search in book titles.
        limit (int, optional): Maximum number of results. Defaults to 20.

    Returns:
        List[Book]: List of Book objects matching the search term.
    """
    return db.query(Book).filter(Book.title.ilike(f"%{search_term}%")).limit(limit).all()


def insert_book(db: Session, title: str, author: str, genre: str, description: str, isbn: str, source: str = "local") -> str:
    """
    **Insert a new book record into the database.**

    This function creates a new **Book** entry with the provided metadata.  
    If successful, it returns the ISBN of the newly added book.  
    You can optionally specify the source of the book data.

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
    """
    **Retrieve all books from the database.**

    This function queries the database and returns a list of **all books** currently stored.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        List[Book]: List of all Book objects.
    """
    return db.query(Book).all()

# -------------------------
# Bookstore / Inventory
# -------------------------
def get_stores_for_book(db: Session, isbn: str) -> List[BookStoreInventory]:
    """
    **Retrieve all bookstores that carry a specific book, sorted by price.**

    This function queries the inventory to find all bookstores stocking the book
    with the given ISBN and returns them in **ascending order of price**.

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
    """
    **Insert or update a book's inventory entry in a bookstore.**

    This function either **creates a new entry** or **updates an existing one** for
    the specified book in the given bookstore. The entry includes the price information.

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
    """
    **Retrieve the most similar books to a given book.**

    This function finds books that are most similar to the reference book
    identified by the provided ISBN. The results are **ordered by similarity score in descending order**.
    You can optionally specify the number of similar books to return.

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
    """
    **Insert or update a similarity score between two books.**

    This function creates a new similarity entry or updates an existing one
    for the pair of books identified by their ISBNs.  
    The similarity score reflects how closely the books are related.

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
    """
    **Log a user's search query in the database.**

    This function records the search performed by a user, including the search term
    and, optionally, the ISBN of a book that matched the query.  
    It helps track user behavior and search trends.

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
    """
    **Retrieve the most recent search queries from the database.**

    This function fetches the latest searches performed by users, ordered by
    **most recent first**. You can optionally specify how many recent searches to return.

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
    """
    **Add or update a user's rating for a book.**

    This function either creates a new rating or updates an existing one
    for the specified book and user.  
    An optional comment can be included alongside the rating value.

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
    **Fetch all ratings for a specific book.**

    This function retrieves all ratings associated with the given ISBN
    and returns them as a list of **RatingResponse** objects, including
    the user's email, rating value, and optional comment.

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
