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
    # First, get the user_id from email
    user = db.query(AppUser).filter(AppUser.email == user_email).first()
    if not user:
        raise ValueError(f"User with email {user_email} not found")
    
    # Call the generic function from db.py
    db_rating = add_or_update_rating(
        db=db,
        user_id=user.user_id,
        book_id=rating.bookId,
        rating_value=rating.rating,
        comment=getattr(rating, "comment", None)
    )
    
    # Return RatingResponse
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
    ratings = db.query(Ratings).join(AppUser).filter(Ratings.book_id == book_id).all()

    return [
        RatingResponse(
            bookId=str(r.book_id),
            user_email=r.user.email,
            rating=r.rating,
            comment=r.comment
        )
        for r in ratings
    ]
