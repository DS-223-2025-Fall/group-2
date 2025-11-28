from fastapi import APIRouter, Depends
from typing import List
from schemas.rating_schema import RatingCreate, RatingResponse
from services.rating_service import add_rating, get_ratings_for_book
from core.security import get_current_user
from sqlalchemy.orm import Session
from db.postgres import get_db

router = APIRouter(prefix="/ratings", tags=["Ratings"])


@router.post("/", response_model=RatingResponse)
def rate_book(
    rating: RatingCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add or update a user's rating for a specific book.

    This endpoint:
    - Requires authentication via `get_current_user`
    - Accepts a rating payload (rating value + comment)
    - Associates the rating with the authenticated user's email
    - Delegates creation/update logic to the rating service

    Args:
        rating (RatingCreate): The rating details submitted by the user.
        user (dict): The currently authenticated user (extracted from JWT).
        db (Session): Database session.

    Returns:
        RatingResponse: The newly created or updated rating.
    """
    return add_rating(db, rating, user["email"])


@router.get("/{book_id}", response_model=List[RatingResponse])
def get_book_ratings(book_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all ratings for a specific book.

    Args:
        book_id (int): The ID of the book whose ratings should be retrieved.
        db (Session): Database session.

    Returns:
        List[RatingResponse]: A list of all ratings for the given book.
    """
    return get_ratings_for_book(db, book_id)
