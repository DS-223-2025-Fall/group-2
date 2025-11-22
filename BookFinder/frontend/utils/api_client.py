"""
API Client for communicating with the backend.
Handles all HTTP requests, error handling, and response transformation.
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List
from config.settings import BACKEND_URL, API_ENDPOINTS, API_TIMEOUT


class APIClient:
    """Client for making requests to the backend API."""
    
    def __init__(self):
        self.base_url = BACKEND_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Make an HTTP request to the backend.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Request body data
            **kwargs: Additional arguments for requests
            
        Returns:
            Response JSON or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout,
                **kwargs
            )
            
            # Raise exception for bad status codes
            response.raise_for_status()
            
            # Return JSON response
            return response.json()
            
        except requests.exceptions.Timeout:
            st.error(f"⏱️ Request timeout - backend took too long to respond")
            return None
            
        except requests.exceptions.ConnectionError:
            st.error(f"🔌 Cannot connect to backend at {self.base_url}")
            return None
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                st.warning("📚 No books found for your search")
            elif response.status_code == 422:
                st.error("❌ Invalid search query")
            else:
                st.error(f"❌ Server error: {response.status_code}")
            return None
            
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    def search_books(self, query: str) -> Optional[List[Dict]]:
        """
        Search for books using the backend API.
        
        Args:
            query: Search query string
            
        Returns:
            List of book dictionaries or None if request fails
        """
        endpoint = API_ENDPOINTS["search_books"]
        params = {"search_query": query}
        
        return self._make_request("GET", endpoint, params=params)
    
    def get_book_ratings(self, book_id: str) -> Optional[Dict]:
        """
        Get ratings for a specific book.
        
        Args:
            book_id: The book's unique identifier
            
        Returns:
            Ratings data or None if request fails
        """
        endpoint = API_ENDPOINTS["get_book_ratings"].format(book_id=book_id)
        return self._make_request("GET", endpoint)
    
    def rate_book(self, book_id: str, rating: float, user_id: Optional[str] = None) -> bool:
        """
        Submit a rating for a book.
        
        Args:
            book_id: The book's unique identifier
            rating: Rating value (typically 1-5)
            user_id: Optional user identifier
            
        Returns:
            True if successful, False otherwise
        """
        endpoint = API_ENDPOINTS["rate_book"]
        data = {
            "book_id": book_id,
            "rating": rating,
        }
        if user_id:
            data["user_id"] = user_id
        
        result = self._make_request("POST", endpoint, data=data)
        return result is not None


# Singleton instance
_api_client = None

def get_api_client() -> APIClient:
    """Get or create the API client singleton."""
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client
