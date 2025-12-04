from schemas.book_schema import BookInfo, BookStoreInfo, FullBookInfo
import requests
import logging
import sys
from pathlib import Path
from typing import List, Optional, Tuple
from db.postgres_service import get_allBooks, get_book_by_isbn, get_stores_for_book
from db.postgres import get_db
from difflib import SequenceMatcher

# Add DS to path and import
DS_PATH = Path(__file__).parent.parent / "ds"
sys.path.insert(0, str(DS_PATH))
from app.book_recommender import BookRecommendationService

logger = logging.getLogger(__name__)

# Initialize DS service once
_ds_service = None

def _get_ds_service():
    global _ds_service
    if _ds_service is None:
        _ds_service = BookRecommendationService()
        if not _ds_service.vector_store.load_index():
            raise ValueError("Vector store not found")
    return _ds_service


def build_full_book_info(book, db_session, match_type=None, is_recommendation=False) -> FullBookInfo:
    """
    Build FullBookInfo with all bookstore information for a book.
    Fetches all stores where this book is available.
    
    Args:
        book (Any): Book model from database.
        db_session (Session): Active database session.
        match_type (str | None): Type of match ("exact", "fuzzy", "semantic", "external").
        is_recommendation (bool): Indicates if this book is a recommendation.

    Returns:
        FullBookInfo: Complete bookstore information and metadata.
    """
    # Get all stores for this book
    store_inventories = get_stores_for_book(db_session, book.ISBN)
    
    # Build store info list
    stores = []
    for inventory in store_inventories:
        store = inventory.store
        store_info = BookStoreInfo(
            storeId=str(store.store_id),
            storeName=store.store_name,
            address=store.address or "",
            city=store.city or "",
            phone=store.phone or "",
            website_url=store.website_url or "",
            email=store.email or "",
            latitude=store.latitude or 0.0,
            longitude=store.longitude or 0.0,
            price=float(inventory.price) if inventory.price else 0.0
        )
        stores.append(store_info)
    
    # Build book info
    book_info = BookInfo(
        bookId=book.ISBN,
        isbn=book.ISBN ,
        bookName=book.title,
        title=book.title,
        author=book.author or "Unknown Author",
        genre=book.genre or "Unknown",
        description=book.description or "",
        language=book.language or "en",
        data_source=book.data_source or "database"
    )
    
    # Build full book info with metadata
    full_book_info = FullBookInfo(
        **book_info.dict(),
        book=book_info,
        stores=stores,
        match_type=match_type,
        is_recommendation=is_recommendation
    )
    
    return full_book_info


def calculate_cer(s1: str, s2: str) -> float:
    """
    Calculate Character Error Rate (CER) between two strings.
    CER is based on Levenshtein distance normalized by length.
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        CER value between 0 (identical) and 1 (completely different)
    """
    s1 = s1.lower().strip()
    s2 = s2.lower().strip()
    
    if not s1 or not s2:
        return 1.0
    
    if s1 == s2:
        return 0.0
    
    # Calculate Levenshtein distance
    len1, len2 = len(s1), len(s2)
    if len1 > len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1
    
    current_row = range(len1 + 1)
    for i in range(1, len2 + 1):
        previous_row, current_row = current_row, [i] + [0] * len1
        for j in range(1, len1 + 1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if s1[j-1] != s2[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    
    # Normalize by the length of the longer string
    levenshtein_distance = current_row[len1]
    cer = levenshtein_distance / max(len1, len2)
    
    return cer


def fuzzy_search_with_cer(search_query: str, all_books: List, threshold: float = 0.3) -> Optional[Tuple[any, float]]:
    """
    Find books using fuzzy matching based on Character Error Rate.
    Returns the best match if CER is below threshold (likely a typo).
    
    Args:
        search_query: User's search query
        all_books: List of all books to search through
        threshold: Maximum CER to consider a match (default 0.3 = 30% error allowed)
        
    Returns:
        Tuple of (best_matching_book, cer_score) or None if no match below threshold
    """
    logger.info(f"Fuzzy CER search for: '{search_query}' (threshold: {threshold})")
    
    search_query = search_query.lower().strip()
    best_match = None
    best_cer = float('inf')
    
    for book in all_books:
        cer = calculate_cer(search_query, book.title)
        
        if cer < best_cer:
            best_cer = cer
            best_match = book
    
    if best_cer <= threshold:
        logger.info(f"Fuzzy match found: '{best_match.title}' (CER: {best_cer:.3f})")
        return (best_match, best_cer)
    else:
        logger.info(f"No fuzzy match below threshold (best CER: {best_cer:.3f})")
        return None

def get_books_service(search_query: str) -> List[FullBookInfo]:
    """
    Main search function with similar books always included.
    
    Process:
    1. Exact match (lowercase) from database
    2. Fuzzy search (CER-based) if no exact match - handles typos
    3. DS semantic search ALWAYS runs to get similar books
    4. External API fallback if no results at all
    
    Returns:
        List of FullBookInfo with metadata:
        - If exact/fuzzy match found: primary match + similar books (no duplicates)
        - If no exact/fuzzy match: only similar books
        - match_type: 'exact', 'fuzzy', 'semantic', or 'external'
        - is_recommendation: False for primary match, True for similar books
    """
    logger.info(f"Search initiated for query: '{search_query}'")
    
    results = []
    match_type = None
    seen_isbns = set()  # Track ISBNs to prevent duplicates
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all books from database
        all_books = get_allBooks(db)
        logger.info(f"Loaded {len(all_books)} books from database")
        
        # Step 1: Try exact match (lowercase)
        logger.info("Step 1: Trying exact match (lowercase)...")
        exact_match = search_book_exact(search_query, all_books)
        
        if exact_match:
            logger.info(f"✓ Exact match found: '{exact_match.title}'")
            results.append(build_full_book_info(exact_match, db, match_type='exact', is_recommendation=False))
            seen_isbns.add(exact_match.ISBN)
            match_type = 'exact'
        else:
            logger.info("No exact match found")
            
            # Step 2: Try fuzzy search (CER)
            logger.info("Step 2: Trying fuzzy search (CER-based)...")
            fuzzy_result = fuzzy_search_with_cer(search_query, all_books, threshold=0.3)
            
            if fuzzy_result:
                book, cer_score = fuzzy_result
                logger.info(f"✓ Fuzzy match found: '{book.title}' (CER: {cer_score:.3f})")
                results.append(build_full_book_info(book, db, match_type='fuzzy', is_recommendation=False))
                seen_isbns.add(book.ISBN)
                match_type = 'fuzzy'
            else:
                logger.info("No fuzzy match found below threshold")
        
        # Step 3: ALWAYS get similar books from DS semantic search
        logger.info("Step 3: Getting similar books via DS semantic search...")
        ds_isbns = search_book_ids_with_ds(search_query, top_k=5)
        
        if ds_isbns:
            logger.info(f"✓ Found {len(ds_isbns)} similar books via DS")
            logger.info(f"ISBNs from DS: {ds_isbns}")
            
            for isbn in ds_isbns:
                # Skip if already added (exact or fuzzy match)
                if isbn in seen_isbns:
                    logger.info(f"Skipping duplicate ISBN: {isbn}")
                    continue
                
                logger.info(f"Looking up ISBN: '{isbn}' (type: {type(isbn).__name__}, len: {len(isbn)})")
                book = get_book_by_isbn(db, isbn)
                if book:
                    logger.info(f"✓ Found book: {book.title} (DB ISBN: '{book.ISBN}', type: {type(book.ISBN).__name__})")
                    results.append(build_full_book_info(book, db, match_type='semantic', is_recommendation=True))
                    seen_isbns.add(isbn)
                else:
                    logger.warning(f"✗ Book not found in DB for ISBN: '{isbn}'")
                    # Try alternative: check if book exists in all_books list
                    for db_book in all_books:
                        if db_book.ISBN == isbn or str(db_book.ISBN) == isbn:
                            logger.info(f"Found in all_books! DB ISBN: '{db_book.ISBN}' (type: {type(db_book.ISBN).__name__})")
                            break
                    else:
                        # Check with stripped version
                        isbn_stripped = isbn.rstrip('.0') if isbn.endswith('.0') else isbn
                        logger.info(f"Trying stripped ISBN: '{isbn_stripped}'")
                        book = get_book_by_isbn(db, isbn_stripped)
                        if book:
                            logger.info(f"✓ Found with stripped ISBN! Book: {book.title}")
                            results.append(build_full_book_info(book, db, match_type='semantic', is_recommendation=True))
                            seen_isbns.add(isbn)
                            seen_isbns.add(isbn_stripped)
            
            # Update match_type if no exact/fuzzy match was found
            if not match_type:
                match_type = 'semantic'
        else:
            logger.info("No DS matches found")
        
        # Step 4: Fall back to external API only if NO results at all
        if not results:
            logger.info("Step 4: No results found, falling back to external API...")
            try:
                external_results = search_book_from_api(search_query)
                if external_results:
                    logger.info(f"✓ Found {len(external_results)} results from external API")
                    results = external_results
                    match_type = 'external'
            except Exception as e:
                logger.error(f"External API search failed: {e}")
        
        logger.info(f"Search complete: {len(results)} results, type: {match_type}")
        return results
        
    finally:
        db.close()


def search_book_exact(search_query: str, all_books: List) -> Optional[any]:
    """
    Search for exact match (case-insensitive) in database.
    
    Args:
        search_query: User's search query
        all_books: List of all books from database
        
    Returns:
        Matching book or None
    """
    query_lower = search_query.lower().strip()
    
    for book in all_books:
        if book.title.lower().strip() == query_lower:
            return book
    
    return None

def search_book_ids_with_ds(search_query: str, top_k: int = 10) -> List[str]:
    """Get ISBNs from DS semantic search. ISBNs are returned as-is from the DS service."""
    try:
        ds_service = _get_ds_service()
        recommendations = ds_service.find_similar_books(query_title=search_query, top_k=top_k)
        
        isbns = []
        for rec in recommendations:
            isbn = str(rec.get('book_id', ''))
            if isbn:
                isbns.append(isbn)
        
        return isbns
    except Exception as e:
        logger.error(f"DS search failed: {e}")
        return []

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
