from fastapi import APIRouter, Depends
from typing import List
from schemas.rating_schema import RatingCreate, RatingResponse
from services.rating_service import add_rating, get_ratings_for_book
from core.security import get_current_user
from sqlalchemy.orm import Session
from db.postgres import get_db


router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
def rate_book(rating: RatingCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)) -> RatingResponse:
    """
    Rate a specific book.

    Args:
        rating (RatingCreate): Rating data containing ISBN and score.
        user (dict): Current authenticated user (injected by Depends).
        db (Session): Database session (injected by Depends).

    Returns:
        RatingResponse: The saved rating, including book and user metadata.
    """
    return add_rating(db, rating, user["email"])

@router.get("/{isbn}", response_model=List[RatingResponse])
def get_book_ratings(isbn: str, db: Session = Depends(get_db)) -> List[RatingResponse]:
    """
    Get all ratings for a specific book.

    Args:
        isbn (str): The ISBN of the book whose ratings should be retrieved.
        db (Session): Database session (injected by Depends).

    Returns:
        List[RatingResponse]: A list of all ratings associated with the given book.
    """
    return get_ratings_for_book(db, isbn)