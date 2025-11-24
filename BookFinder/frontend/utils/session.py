"""
Session state management for the FindMyRead application.
Handles all state initialization and navigation functions.
"""
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables if they don't exist."""
    if "view" not in st.session_state:
        st.session_state["view"] = "home"
    if "last_query" not in st.session_state:
        st.session_state["last_query"] = ""
    if "exact" not in st.session_state:
        st.session_state["exact"] = []
    if "suggestions" not in st.session_state:
        st.session_state["suggestions"] = []
    if "selected_book_id" not in st.session_state:
        st.session_state["selected_book_id"] = None
    
    # Authentication state
    if "auth_token" not in st.session_state:
        st.session_state["auth_token"] = None
    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = None


def sync_query_params():
    """Sync session state from URL query parameters for browser navigation."""
    query_params = st.query_params
    
    # Handle OAuth callback parameters (token, email, name)
    if "token" in query_params:
        st.session_state["auth_token"] = query_params["token"]
        if "email" in query_params:
            st.session_state["user_email"] = query_params["email"]
        if "name" in query_params:
            st.session_state["user_name"] = query_params["name"]
        
        # Set success message
        st.session_state["login_success_message"] = "Successfully logged in!"
        
        # Clear the callback params from URL and redirect to home
        st.query_params.clear()
        st.session_state["view"] = "home"
        st.rerun()
        return
    
    # Handle view parameter
    if "view" in query_params:
        param_view = query_params["view"]
        if param_view in ["home", "results", "detail"]:
            st.session_state["view"] = param_view
            
            # Handle detail view
            if param_view == "detail" and "book_id" in query_params:
                try:
                    st.session_state["selected_book_id"] = int(query_params["book_id"])
                except ValueError:
                    pass
            
            # Handle results view - restore search if we have a query
            if param_view == "results" and "q" in query_params:
                search_query = query_params["q"]
                # Only re-search if the query is different from what we have
                if st.session_state.get("last_query") != search_query:
                    from utils.search import simple_search
                    st.session_state["last_query"] = search_query
                    exact, suggestions = simple_search(search_query)
                    st.session_state["exact"] = exact
                    st.session_state["suggestions"] = suggestions
    elif "q" not in query_params:
        # No view param and no query - default to home
        if st.session_state.get("view") not in ["home", "results", "detail"]:
            st.session_state["view"] = "home"


def go_home():
    """Navigate to home view and clear all search data."""
    st.session_state["view"] = "home"
    st.session_state["last_query"] = ""
    st.session_state["exact"] = []
    st.session_state["suggestions"] = []
    st.session_state["selected_book_id"] = None
    # Update URL
    st.query_params.clear()


def go_to_detail(book_id: int):
    """
    Navigate to book detail view.
    
    Args:
        book_id: The ID of the book to display
    """
    if book_id is None:
        st.error("Error: Book ID is missing")
        return
        
    st.session_state["view"] = "detail"
    st.session_state["selected_book_id"] = book_id
    # Update URL - keep search query if it exists for back navigation
    st.query_params["view"] = "detail"
    st.query_params["book_id"] = str(book_id)


def go_back_to_home():
    """Navigate back to home page."""
    st.session_state["view"] = "home"
    st.session_state["last_query"] = ""
    st.session_state["exact"] = []
    st.session_state["suggestions"] = []
    st.session_state["selected_book_id"] = None


def go_to_login():
    """Navigate to login page."""
    st.session_state["view"] = "login"
    # Update URL
    st.query_params.clear()
    st.query_params["view"] = "login"


def is_authenticated() -> bool:
    """Check if user is currently authenticated."""
    return st.session_state.get("auth_token") is not None


def login(token: str, email: str, name: str = None):
    """
    Store authentication credentials in session.
    
    Args:
        token: JWT authentication token
        email: User's email address
        name: User's display name (optional)
    """
    st.session_state["auth_token"] = token
    st.session_state["user_email"] = email
    st.session_state["user_name"] = name


def logout():
    """Clear authentication credentials from session."""
    st.session_state["auth_token"] = None
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None


def get_auth_token() -> str:
    """Get the current authentication token."""
    return st.session_state.get("auth_token")


def get_user_info() -> dict:
    """Get current user information."""
    return {
        "email": st.session_state.get("user_email"),
        "name": st.session_state.get("user_name")
    }
