from typing_extensions import Optional
from pydantic import BaseModel

class RatingCreate(BaseModel):
    bookId: str
    rating: int
    comment: Optional[str] = None

class RatingResponse(BaseModel):
    bookId: str
    user_email: str
    rating: int
    comment: Optional[str] = None