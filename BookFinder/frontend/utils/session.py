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


def sync_query_params():
    """Sync session state from URL query parameters for browser navigation."""
    query_params = st.query_params
    if "view" in query_params:
        param_view = query_params["view"]
        if param_view in ["home", "results", "detail"]:
            st.session_state["view"] = param_view
            if param_view == "detail" and "book_id" in query_params:
                try:
                    st.session_state["selected_book_id"] = int(query_params["book_id"])
                except ValueError:
                    pass


def go_home():
    """Navigate to home view and clear all search data."""
    st.session_state["view"] = "home"
    st.session_state["last_query"] = ""
    st.session_state["exact"] = []
    st.session_state["suggestions"] = []
    st.session_state["selected_book_id"] = None
    st.query_params.clear()


def go_to_detail(book_id: int):
    """
    Navigate to book detail view.
    
    Args:
        book_id: The ID of the book to display
    """
    st.session_state["view"] = "detail"
    st.session_state["selected_book_id"] = book_id
    st.query_params.update({"view": "detail", "book_id": str(book_id)})


def go_back_to_results():
    """Navigate back to search results view."""
    st.session_state["view"] = "results"
    st.query_params.update({"view": "results"})
