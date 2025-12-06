from fastapi import APIRouter, Query
from schemas.book_schema import FullBookInfo
from services.books_service import get_books_service
# from services.similarity_service import get_books_similarity_service
from typing import List, Dict, Any

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/search", response_model=List[FullBookInfo])
def get_books(search_query: str = Query(..., description="Search term for books")):
    """
    **Search for books using a 3-step process:** *exact → fuzzy → semantic*.

    This function returns a list of books including **main results** and **recommendations**,
    with relevant metadata for each book.

    Each book includes the following fields:
    - **match_type**: `"exact"`, `"fuzzy"`, `"semantic"`, or `"external"`.
    - **is_recommendation**: `true` for recommended books, `false` for main search results.
    """
    return get_books_service(search_query)