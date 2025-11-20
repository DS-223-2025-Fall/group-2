from schemas.book_schema import BookInfo, BookStoreInfo, FullBookInfo
import requests
from typing import List
from db.postgres_service import get_allBooks
from typing import List
from difflib import SequenceMatcher

def get_books_service(search_query) -> list[FullBookInfo]:
    local_results = search_book_in_db(search_query)
    if local_results:
        return local_results
    
    print("No local match found. Querying external API...")
    return search_book_from_api(search_query)

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_book_in_db(search_query: str) -> List[FullBookInfo]:
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
        description = doc.get("first_sentence", {}).get("value", "") \
            if isinstance(doc.get("first_sentence"), dict) else doc.get("first_sentence", "")
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

        results.append(FullBookInfo(
            **book_info.dict(),
            book=book_info,
            stores=get_dummy_stores()
        ))

    return results
