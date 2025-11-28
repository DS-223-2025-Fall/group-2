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
    Add a new rating or update an existing one for a specific book.

    This function:
    - Fetches the user by email to get their user_id.
    - Calls the generic `add_or_update_rating` DB function.
    - Returns the result wrapped in a `RatingResponse` schema.

    Args:
        db (Session): SQLAlchemy database session.
        rating (RatingCreate): Rating data containing bookId, rating, and optional comment.
        user_email (str): Email of the user submitting the rating.

    Returns:
        RatingResponse: The created or updated rating record.

    Raises:
        ValueError: If the user with the given email does not exist.
    """
    user = db.query(AppUser).filter(AppUser.email == user_email).first()
    if not user:
        raise ValueError(f"User with email {user_email} not found")

    db_rating = add_or_update_rating(
        db=db,
        user_id=user.user_id,
        book_id=rating.bookId,
        rating_value=rating.rating,
        comment=getattr(rating, "comment", None)
    )

    return RatingResponse(
        bookId=str(db_rating.book_id),
        user_email=user_email,
        rating=db_rating.rating,
        comment=db_rating.comment
    )


# -------------------------
# Get all ratings for a book
# -------------------------
def get_ratings_for_book(db: Session, book_id: str) -> List[RatingResponse]:
    """
    Retrieve all ratings associated with a specific book.

    Args:
        db (Session): SQLAlchemy database session.
        book_id (str): ID of the book whose ratings should be fetched.

    Returns:
        List[RatingResponse]: List of rating entries for the given book.
    """
    ratings = (
        db.query(Ratings)
        .join(AppUser)
        .filter(Ratings.book_id == book_id)
        .all()
    )

    return [
        RatingResponse(
            bookId=str(r.book_id),
            user_email=r.user.email,
            rating=r.rating,
            comment=r.comment
        )
        for r in ratings
    ]
