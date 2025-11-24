"""
Home page component for FindMyRead application.
Displays hero section with search bar and bookstore strip.
"""
import streamlit as st
from data.books import BOOKSTORES
from utils.search import simple_search


def render_home():
    """Render the home page view."""
    # Hero section
    st.markdown(
        """
        <div class="hero-wrapper">
            <div class="hero-title">Discover Your Next<br/>Literary Journey</div>
            <div class="hero-subtitle">
                Find your next read — or the closest one.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Search form
    center = st.columns([1, 2, 1])[1]
    with center:
        with st.form("hero_search", clear_on_submit=True):
            c1, c2 = st.columns([7, 2])
            with c1:
                query = st.text_input(
                    "",
                    placeholder="Search for any book…",
                    label_visibility="collapsed",
                    key="hero_query",
                )
            with c2:
                submit = st.form_submit_button("Search")

    # Handle search submission
    if submit and query:
        exact, suggestions = simple_search(query)
        st.session_state["view"] = "results"
        st.session_state["last_query"] = query
        st.session_state["exact"] = exact
        st.session_state["suggestions"] = suggestions
        st.rerun()

    # Bookstore strip at bottom
    items = "".join(
        f'<div class="store-strip-item"><span class="store-strip-icon"></span><span>{store}</span></div>'
        for store in BOOKSTORES
    )
    st.markdown(
        f'''
        <div class="store-strip-container">
            <div class="store-strip-label">Searching across trusted bookstores</div>
            <div class="store-strip-badges">{items}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )
