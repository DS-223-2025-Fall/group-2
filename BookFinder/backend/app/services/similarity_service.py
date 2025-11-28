import logging
import sys
from pathlib import Path
from schemas.book_schema import FullBookInfo, BookInfo, BookStoreInfo
from db.postgres_service import get_book_by_isbn, get_stores_for_book
from db.postgres import get_db
from typing import List

# Add DS to path and import
DS_PATH = Path(__file__).parent.parent / "ds"
sys.path.insert(0, str(DS_PATH))
from app.book_recommender import BookRecommendationService

logger = logging.getLogger(__name__)
_ds_service = None

def _get_ds_service():
    global _ds_service
    if _ds_service is None:
        _ds_service = BookRecommendationService()
        if not _ds_service.vector_store.load_index():
            raise ValueError("Vector store not found")
    return _ds_service


def build_full_book_info_similarity(book, db_session) -> FullBookInfo:
    """
    Build FullBookInfo with all bookstore information for similarity results.
    These are always recommendations from semantic search.
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
        bookId=str(book.ISBN),
        bookName=book.title,
        isbn=book.ISBN or "",
        title=book.title,
        author=book.author or "Unknown Author",
        genre=book.genre or "Unknown",
        description=book.description or "",
        language=book.language or "en",
        data_source=book.data_source or "database"
    )
    
    # Build full book info with metadata (similarity results are always recommendations)
    full_book_info = FullBookInfo(
        **book_info.dict(),
        book=book_info,
        stores=stores,
        match_type='semantic',
        is_recommendation=True
    )
    
    return full_book_info


def get_books_similarity_service(book_id: str) -> list[FullBookInfo]:
    """
    Get books similar to a specific book using DS semantic search
    
    Args:
        book_id: ID of the book to find similar books for
        
    Returns:
        List of similar books with full store information
    """
    logger.info(f"Fetching similar books for book ID: {book_id}")
    
    db = next(get_db())
    
    try:
        # Get the book from database first to get its title
        query_book = get_book_by_isbn(db, int(book_id))
        if not query_book:
            logger.warning(f"Book ID {book_id} not found in database")
            return []
        
        # Get DS recommendations using the book title
        ds_service = _get_ds_service()
        recommendations = ds_service.find_similar_books(query_title=query_book.title, top_k=10)
        
        if not recommendations:
            logger.warning(f"No similar books found for book ID: {book_id}")
            return []
        
        # Get the recommended books (excluding the query book itself)
        results = []
        for rec in recommendations:
            rec_book_id = rec.get('book_id')
            
            # Skip if it's the same book
            if str(rec_book_id) == str(book_id):
                continue
            
            # Fetch book from database
            try:
                book = get_book_by_isbn(db, int(rec_book_id))
                if book:
                    results.append(build_full_book_info_similarity(book, db))
                else:
                    logger.warning(f"Book ID {rec_book_id} not found in database")
            except Exception as e:
                logger.error(f"Error fetching book {rec_book_id}: {e}")
        
        logger.info(f"✓ Found {len(results)} similar books for book ID: {book_id}")
        return results
        
    except Exception as e:
        logger.error(f"Error in similarity service: {e}", exc_info=True)
        return []
    finally:
        db.close()
