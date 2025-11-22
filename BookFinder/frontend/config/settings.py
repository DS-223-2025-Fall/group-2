"""
Application configuration settings.
"""
import os

# Page configuration
PAGE_TITLE = "FindMyRead"
PAGE_ICON = "📚"
LAYOUT = "wide"

# API Configuration
# Reads from environment variable first, falls back to localhost for development
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# API Endpoints
API_ENDPOINTS = {
    "search_books": "/api/books/search",
    "get_book_ratings": "/api/ratings/{book_id}",
    "rate_book": "/api/ratings/",
    "auth_google": "/api/auth/google",
    "auth_callback": "/api/auth/google/callback",
}

# Request timeout (seconds)
API_TIMEOUT = 10

# Enable mock data fallback if API fails
USE_MOCK_FALLBACK = True
