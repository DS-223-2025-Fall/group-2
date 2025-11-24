"""
Utility functions for search and data operations.
"""
import random
import streamlit as st
from data.books import BOOKS
from utils.api_client import get_api_client
from utils.transformers import transform_books_list_from_api
from config.settings import USE_MOCK_FALLBACK


def simple_search(query: str):
    """
    Search for books matching the query using the backend API.
    Falls back to mock data if API fails and USE_MOCK_FALLBACK is True.
    
    Args:
        query: Search query string
        
    Returns:
        Tuple of (exact_matches, suggestions)
    """
    q = query.lower().strip()
    if not q:
        return [], []
    
    # Try to fetch from API
    api_client = get_api_client()
    
    api_response = api_client.search_books(q)
    
    if api_response is not None:
        # API call successful - transform the data
        books = transform_books_list_from_api(api_response)
        
        if books:
            # Return all results as exact matches
            # Backend already does the filtering
            return books, []
        else:
            # No results from API
            return [], []
    
    # API failed - use mock fallback if enabled
    if USE_MOCK_FALLBACK:
        st.info("📚 Using offline data (backend unavailable)")
        return _search_mock_data(q)
    else:
        # No fallback, return empty results
        return [], []


def _search_mock_data(query: str):
    """
    Fallback search using mock data.
    
    Args:
        query: Search query string (lowercase, stripped)
        
    Returns:
        Tuple of (exact_matches, suggestions)
    """
    # Find exact matches
    exact = [b for b in BOOKS if query in b["title"].lower() or query in b["author"].lower()]
    
    # If exact matches found, return remaining books as suggestions
    if exact:
        suggestions = [b for b in BOOKS if b not in exact]
    else:
        # No exact matches, return random suggestions
        suggestions = random.sample(BOOKS, min(3, len(BOOKS)))
    
    return exact, suggestions


def get_book_by_id(book_id: str):
    """
    Retrieve a book by its ID.
    First checks API, then falls back to mock data if enabled.
    
    Args:
        book_id: The book's unique identifier (string for API compatibility)
        
    Returns:
        Book dict or None if not found
    """
    # For now, we don't have a get-by-id endpoint
    # So we'll search through session state if available
    # or fall back to mock data
    
    # Try to find in mock data first (for backwards compatibility)
    for book in BOOKS:
        if str(book.get("id")) == str(book_id):
            return book
    
    # If not found and we have session state with search results, check there
    if "exact" in st.session_state:
        for book in st.session_state["exact"]:
            if str(book.get("id")) == str(book_id):
                return book
    
    if "suggestions" in st.session_state:
        for book in st.session_state["suggestions"]:
            if str(book.get("id")) == str(book_id):
                return book
    
    return None
