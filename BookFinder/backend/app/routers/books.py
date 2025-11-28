from fastapi import APIRouter, Query
from schemas.book_schema import FullBookInfo
from services.books_service import get_books_service
from typing import List

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/search", response_model=List[FullBookInfo])
def get_books(search_query: str = Query(..., description="Search term for books")):
    """
    Search for books using a free-text query.

    This endpoint forwards the search term to the books service,
    which performs the actual database lookup and returns a list
    of matching books enriched with full metadata.

    Args:
        search_query (str): The search term used to filter books.  
            This may include partial titles, authors, or keywords.

    Returns:
        List[FullBookInfo]: A list of books matching the search query.
    """
    return get_books_service(search_query)
