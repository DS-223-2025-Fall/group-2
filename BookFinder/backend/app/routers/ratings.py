from fastapi import APIRouter, Depends
from typing import List
from schemas.rating_schema import RatingCreate, RatingResponse
from services.rating_service import add_rating, get_ratings_for_book
from core.security import get_current_user
from sqlalchemy.orm import Session
from db.postgres import get_db


router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse)
def rate_book(rating: RatingCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_rating(db, rating, user["email"])

@router.get("/{isbn}", response_model=List[RatingResponse])
def get_book_ratings(isbn: str, db: Session = Depends(get_db)):
    return get_ratings_for_book(db, isbn)