from fastapi import APIRouter, Query
from schemas.book_schema import FullBookInfo
from services.books_service import get_books_service
from services.similarity_service import get_books_similarity_service
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/search", response_model=List[FullBookInfo])
def get_books(search_query: str = Query(..., description="Search term for books")):
    return get_books_service(search_query)

@router.get("/similarity/{book_id}", response_model=List[FullBookInfo])
def get_book_ratings(book_id: str):
    return get_books_similarity_service(book_id)