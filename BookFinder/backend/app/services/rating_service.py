from typing import List
from sqlalchemy.orm import Session
from db.postgres import get_db
from db.postgres_service import add_or_update_rating
from schemas.rating_schema import RatingResponse, RatingCreate
from db.models import Ratings, AppUser

# -------------------------
# Add or update rating
# -------------------------
def add_rating(db: Session, rating: RatingCreate, user_email: str) -> RatingResponse:
    """
    Add or update a user's rating for a specific book.

    Args:
        db (Session): Active SQLAlchemy database session.
        rating (RatingCreate): Rating details including bookId, rating value, and optional comment.
        user_email (str): Email of the authenticated user submitting the rating.

    Returns:
        RatingResponse: The saved or updated rating, including bookId, user email, rating value, and comment.
    """

    # First, get the user_id from email
    user = db.query(AppUser).filter(AppUser.email == user_email).first()
    if not user:
        raise ValueError(f"User with email {user_email} not found")
    
    # Call the generic function from db.py
    db_rating = add_or_update_rating(
        db=db,
        user_id=user.user_id,
        isbn=rating.bookId,
        rating_value=rating.rating,
        comment=getattr(rating, "comment", None)
    )
    
    # Return RatingResponse
    return RatingResponse(
        bookId=str(db_rating.ISBN),
        user_email=user_email,
        rating=db_rating.rating,
        comment=db_rating.comment
    )

# -------------------------
# Get all ratings for a book
# -------------------------
def get_ratings_for_book(db: Session, isbn: str) -> List[RatingResponse]:
    """
    Retrieve all ratings for a given book.

    Args:
        db (Session): Active SQLAlchemy database session.
        isbn (str): The ISBN of the book whose ratings should be returned.

    Returns:
        List[RatingResponse]: A list of ratings submitted for the specified book,
        each including bookId, user email, rating value, and comment.
    """
    ratings = db.query(Ratings).join(AppUser).filter(Ratings.ISBN == isbn).all()

    return [
        RatingResponse(
            bookId=str(r.ISBN),
            user_email=r.user.email,
            rating=r.rating,
            comment=r.comment
        )
        for r in ratings
    ]
