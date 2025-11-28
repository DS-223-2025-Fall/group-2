"""
API Client for communicating with the backend.
Handles all HTTP requests, error handling, and response transformation.
"""
import requests
import streamlit as st
from typing import Optional, Dict, Any, List
from config.settings import BACKEND_DOCKER_URL, API_ENDPOINTS, API_TIMEOUT


class APIClient:
    """Client for making requests to the backend API."""
    
    def __init__(self, auth_token: Optional[str] = None):
        self.base_url = BACKEND_DOCKER_URL
        self.timeout = API_TIMEOUT
        self.session = requests.Session()
        # Set default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })
        # Set authentication token if provided
        if auth_token:
            self.set_auth_token(auth_token)
    
    def set_auth_token(self, token: str):
        """Set the authentication token for API requests."""
        self.session.headers["Authorization"] = f"Bearer {token}"
    
    def clear_auth_token(self):
        """Clear the authentication token."""
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]
    
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
        print(f"Making {method} request to {url} with params={params} and data={data}")
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
            if response.status_code == 401:
                st.error("🔒 Authentication required - Please log in to rate books")
            elif response.status_code == 404:
                st.warning("📚 No books found for your search")
            elif response.status_code == 422:
                # Validation error - could be from any endpoint
                error_detail = response.json().get("detail", "Invalid data format")
                st.error(f"❌ Validation error: {error_detail}")
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
        # TODO: Remove dummy data and use actual API
        endpoint = API_ENDPOINTS["search_books"]
        params = {"search_query": query}
        return self._make_request("GET", endpoint, params=params)
        
        # # Return dummy books for testing - matching backend API format
        # return [
        #     {
        #         "bookId": "1",
        #         "title": "The Great Gatsby",
        #         "author": "F. Scott Fitzgerald",
        #         "description": "A classic novel of the Jazz Age, exploring themes of wealth, love, and the American Dream.",
        #         "genre": "Fiction",
        #         "language": "English",
        #         "isbn": "978-0-7432-7356-5",
        #         "stores": [{"storeName": "Zangak"}]
        #     },
        #     {
        #         "bookId": "2",
        #         "title": "To Kill a Mockingbird",
        #         "author": "Harper Lee",
        #         "description": "A gripping tale of racial injustice and childhood innocence in the American South.",
        #         "genre": "Fiction",
        #         "language": "English",
        #         "isbn": "978-0-06-112008-4",
        #         "stores": [{"storeName": "Books.am"}]
        #     },
        #     {
        #         "bookId": "3",
        #         "title": "1984",
        #         "author": "George Orwell",
        #         "description": "A dystopian masterpiece about totalitarianism, surveillance, and individual freedom.",
        #         "genre": "Science Fiction",
        #         "language": "English",
        #         "isbn": "978-0-452-28423-4",
        #         "stores": [{"storeName": "Bookinist"}]
        #     },
        #     {
        #         "bookId": "4",
        #         "title": "Pride and Prejudice",
        #         "author": "Jane Austen",
        #         "description": "A timeless romance exploring class, marriage, and society in Regency England.",
        #         "genre": "Romance",
        #         "language": "English",
        #         "isbn": "978-0-14-143951-8",
        #         "stores": [{"storeName": "Noyan Tapan"}]
        #     },
        #                 {
        #         "bookId": "5",
        #         "title": "Pride and Prejudice",
        #         "author": "Jane Austen",
        #         "description": "A timeless romance exploring class, marriage, and society in Regency England.",
        #         "genre": "Romance",
        #         "language": "English",
        #         "isbn": "978-0-14-143951-8",
        #         "stores": [{"storeName": "Noyan Tapan"}]
        #     },
        #                 {
        #         "bookId": "6",
        #         "title": "Pride and Prejudice",
        #         "author": "Jane Austen",
        #         "description": "A timeless romance exploring class, marriage, and society in Regency England.",
        #         "genre": "Romance",
        #         "language": "English",
        #         "isbn": "978-0-14-143951-8",
        #         "stores": [{"storeName": "Noyan Tapan"}]
        #     }
        # ]
    
    def get_book_ratings(self, book_id: str) -> Optional[List[Dict]]:
        """
        Get all ratings for a specific book.
        
        Args:
            book_id: The book's unique identifier
            
        Returns:
            List of rating dictionaries or None if request fails
            [
                {
                    "bookId": "string",
                    "user_email": "string",
                    "rating": 0,
                    "comment": "string"
                }
            ]
        """
        endpoint = API_ENDPOINTS["get_book_ratings"].format(book_id=book_id)
        return self._make_request("GET", endpoint)
    
    def rate_book(
        self, 
        book_id: str, 
        rating: float, 
        comment: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Submit a rating for a book.
        
        Args:
            book_id: The book's unique identifier
            rating: Rating value (0-5)
            comment: Optional text review/comment
            
        Returns:
            Rating response dict or None if request fails
            {
                "bookId": "string",
                "user_email": "string",
                "rating": 0,
                "comment": "string"
            }
        """
        endpoint = API_ENDPOINTS["rate_book"]
        data = {
            "bookId": book_id,
            "rating": rating,
        }
        if comment:
            data["comment"] = comment
        
        result = self._make_request("POST", endpoint, data=data)
        return result


# Singleton instance
_api_client = None

def get_api_client(auth_token: Optional[str] = None) -> APIClient:
    """
    Get or create the API client singleton.
    
    Args:
        auth_token: Optional authentication token to set
        
    Returns:
        APIClient instance
    """
    global _api_client
    if _api_client is None:
        _api_client = APIClient(auth_token=auth_token)
    elif auth_token:
        _api_client.set_auth_token(auth_token)
    return _api_client
