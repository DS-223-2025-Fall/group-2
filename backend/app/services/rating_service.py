from typing import List
from schemas.rating_schema import RatingResponse, RatingCreate

ratings_db: List[RatingResponse] = [
    RatingResponse(bookId="b1", user_email="alice@example.com", rating=5, comment="Great book!"),
    RatingResponse(bookId="b1", user_email="bob@example.com", rating=4, comment="Enjoyed it."),
    RatingResponse(bookId="b2", user_email="charlie@example.com", rating=3, comment="It was okay."),
    RatingResponse(bookId="b2", user_email="alice@example.com", rating=4, comment="Good read."),
    RatingResponse(bookId="b3", user_email="bob@example.com", rating=2, comment="Not my type."),
] # Get from DB later

def add_rating(rating: RatingCreate, user_email: str) -> RatingResponse:
    for r in ratings_db:
        if r.bookId == rating.bookId and r.user_email == user_email:
            r.rating = rating.rating
            return r
    
    new_rating = RatingResponse(bookId=rating.bookId, user_email=user_email, rating=rating.rating)
    ratings_db.append(new_rating)
    return new_rating

def get_ratings_for_book(book_id: str) -> List[RatingResponse]:
    return [r for r in ratings_db if r.bookId == book_id]