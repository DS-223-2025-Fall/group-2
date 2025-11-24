"""
Application configuration settings.
"""
import os

# Page configuration
PAGE_TITLE = "FindMyRead"
PAGE_ICON = "📚"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "collapsed"
MENU_ITEMS = {
    'Get Help': None,
    'Report a bug': None,
    'About': None
}

# API Configuration
# Reads from environment variable first, falls back to localhost for development
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Backend URL for browser redirects (OAuth)
# This is the URL accessible from user's browser, not from inside Docker
# For Docker: use http://localhost:8008 (host machine port)
# For local dev: use http://localhost:8000
BACKEND_BROWSER_URL = os.getenv("BACKEND_BROWSER_URL", "http://localhost:8000")

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
USE_MOCK_FALLBACK = False
