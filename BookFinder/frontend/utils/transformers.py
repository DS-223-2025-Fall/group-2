"""
Data transformation utilities.
Converts backend API responses to frontend data models.
"""
from typing import Dict, List, Any, Optional


def transform_book_from_api(api_book: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform a book from the backend API format to our frontend format.
    
    Backend format:
    {
        "bookId": "string",
        "bookName": "string",
        "isbn": "string",
        "title": "string",
        "author": "string",
        "genre": "string",
        "description": "string",
        "language": "string",
        "data_source": "string",
        "stores": [...],
        "book": {...}
    }
    
    Frontend format:
    {
        "id": "string",
        "title": "string",
        "author": "string",
        "description": "string",
        "long_description": "string",
        "rating": float,
        "genre": "string",
        "language": "string",
        "isbn": "string",
        "store": {
            "name": "string",
            "price": int,
            "currency": "AMD"
        },
        "stores": [...]  # Keep all stores too
    }
    """
    # Get the primary store (first one if multiple exist)
    stores = api_book.get("stores", [])
    primary_store = stores[0] if stores else None
    
    # Create store object for our format
    store_data = {
        "name": primary_store.get("storeName", "Unknown Store") if primary_store else "Unknown Store",
        "price": int(primary_store.get("price", 0)) if primary_store else 0,  # Get price from backend
        "currency": "AMD"
    }
    
    # If store has additional data, include it
    if primary_store:
        store_data["address"] = primary_store.get("address", "")
        store_data["phone"] = primary_store.get("phone", "")
        store_data["website"] = primary_store.get("website_url", "")
    
    # Transform to our format
    return {
        "id": api_book.get("bookId", ""),
        "title": api_book.get("title", "") or api_book.get("bookName", "Untitled"),
        "author": api_book.get("author", "Unknown Author"),
        "description": api_book.get("description", "No description available.")[:200],  # Short version
        "long_description": api_book.get("description", "No description available."),  # Full version
        "rating": 4.0,  # Default rating (will be updated from ratings API)
        "genre": api_book.get("genre", "General"),
        "language": api_book.get("language", "Unknown"),
        "isbn": api_book.get("isbn", ""),
        "store": store_data,
        "stores": stores,  # Keep all stores for potential future use
        "data_source": api_book.get("data_source", ""),
        "match_type": api_book.get("match_type", None),  # Metadata from backend
        "is_recommendation": api_book.get("is_recommendation", False),  # Metadata from backend
    }


def transform_books_list_from_api(api_books: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transform a list of books from API format to frontend format.
    
    Args:
        api_books: List of books in backend format
        
    Returns:
        List of books in frontend format
    """
    return [transform_book_from_api(book) for book in api_books]


def get_store_info_summary(stores: List[Dict[str, Any]]) -> str:
    """
    Create a summary string of all stores carrying a book.
    
    Args:
        stores: List of store objects
        
    Returns:
        Formatted string like "Available at: Store1, Store2, Store3"
    """
    if not stores:
        return "No stores available"
    
    store_names = [store.get("storeName", "Unknown") for store in stores]
    if len(store_names) == 1:
        return f"Available at: {store_names[0]}"
    elif len(store_names) <= 3:
        return f"Available at: {', '.join(store_names)}"
    else:
        return f"Available at: {', '.join(store_names[:3])} and {len(store_names) - 3} more"
