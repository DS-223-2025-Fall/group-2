from fastapi import APIRouter, Depends
from typing import List
from schemas.rating_schema import RatingCreate, RatingResponse
from services.rating_service import add_rating, get_ratings_for_book
from core.security import get_current_user

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
def rate_book(rating: RatingCreate, user: dict = Depends(get_current_user)):
    return add_rating(rating, user["email"])

@router.get("/{book_id}", response_model=List[RatingResponse])
def get_book_ratings(book_id: str):
    return get_ratings_for_book(book_id)