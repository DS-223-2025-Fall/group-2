from schemas.book_schema import BookInfo, BookStoreInfo, FullBookInfo
import requests
from typing import List
from db.postgres_service import get_allBooks
from difflib import SequenceMatcher


def get_books_service(search_query: str) -> List[FullBookInfo]:
    """
    High-level book search service.

    This function:
    1. Attempts to find matching books in the local database using fuzzy matching.
    2. If no meaningful results are found, it queries the external OpenLibrary API.

    Args:
        search_query (str): The user-provided search term.

    Returns:
        List[FullBookInfo]: A list of locally found or externally fetched books.
    """
    local_results = search_book_in_db(search_query)
    if local_results:
        return local_results

    print("No local match found. Querying external API...")
    return search_book_from_api(search_query)


def similarity(a: str, b: str) -> float:
    """
    Compute similarity score between two strings using SequenceMatcher.

    Args:
        a (str): First string.
        b (str): Second string.

    Returns:
        float: A similarity ratio between 0 and 1.
    """
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_book_in_db(search_query: str) -> List[FullBookInfo]:
    """
    Fuzzy search for books in the local database.

    This function:
    - Retrieves all books from the database.
    - Computes a similarity score against the search query.
    - Returns the top 10 matches with a similarity score ≥ 0.7.

    Args:
        search_query (str): User search term.

    Returns:
        List[FullBookInfo]: A list of matched books from the local DB.
    """
    books: List[FullBookInfo] = get_allBooks()
    scored_books = []

    for book in books:
        score = similarity(search_query, book.title)
        if score >= 0.7:
            scored_books.append((score, book))

    scored_books.sort(key=lambda x: x[0], reverse=True)
    return [book for _, book in scored_books[:10]]


def get_dummy_stores() -> List[BookStoreInfo]:
    return [
        BookStoreInfo(
            storeId="s1",
            storeName="Books & Co",
            address="123 Main St",
            city="New York",
            phone="+1 555 123456",
            website_url="https://booksco.example.com",
            email="info@booksco.example.com",
            latitude=40.7128,
            longitude=-74.0060
        )
    ]


def search_book_from_api(search_query: str) -> List[FullBookInfo]:
    """
    Query the OpenLibrary API for books.

    This function calls OpenLibrary’s search endpoint and transforms the results
    into FullBookInfo objects with consistent formatting.

    Args:
        search_query (str): The search term used for querying OpenLibrary.

    Returns:
        List[FullBookInfo]: A list of books returned by OpenLibrary.

    Raises:
        ValueError: If the API fails or returns no books.
    """
    url = f"https://openlibrary.org/search.json?title={search_query}&limit=10"
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError("External API failed.")

    docs = response.json().get("docs", [])
    if not docs:
        raise ValueError("No books found in external API.")

    results = []

    for doc in docs:
        title = doc.get("title", "Unknown Title")
        author = doc.get("author_name", ["Unknown"])[0]
        isbn = doc.get("isbn", [""])[0] if "isbn" in doc else ""

        # Handle description formats
        raw_desc = doc.get("first_sentence")
        description = (
            raw_desc.get("value", "")
            if isinstance(raw_desc, dict)
            else raw_desc or ""
        )

        language = doc.get("language", ["en"])[0]
        genre = doc.get("subject", ["Unknown"])[0]

        book_info = BookInfo(
            bookId=f"ext-{isbn or title.replace(' ', '_')}",
            bookName=title,
            isbn=isbn,
            title=title,
            author=author,
            genre=genre,
            description=description,
            language=language,
            data_source="OpenLibrary"
        )

        results.append(
            FullBookInfo(
                **book_info.dict(),
                book=book_info,
                stores=get_dummy_stores()
            )
        )

    return results
