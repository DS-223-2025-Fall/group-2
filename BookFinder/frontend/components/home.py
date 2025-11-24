"""
Home page component for FindMyRead application.
Displays hero section with search bar and bookstore strip.
"""
import streamlit as st
from data.books import BOOKSTORES
from utils.search import simple_search


def render_home():
    """Render the home page view."""
    # Hero section with fade-in animation
    st.markdown(
        """
        <div class="hero-wrapper fade-in">
            <div class="hero-title">Discover Your Next<br/>Literary Journey</div>
            <div class="hero-subtitle">
                Find your next read — or the closest one.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered search form (the beige container is now handled purely by CSS)
    center = st.columns([1, 6, 1])[1]
    with center:
        with st.form("hero_search"):
            c1, c2 = st.columns([7, 2])
            with c1:
                query = st.text_input(
                    "",
                    placeholder="🔍 Search for any book…",
                    label_visibility="collapsed",
                    key="hero_query",
                )
            with c2:
                submit = st.form_submit_button("Search", use_container_width=True)

    # Handle search submission
    if submit and query:
        exact, suggestions = simple_search(query)
        st.session_state["view"] = "results"
        st.session_state["last_query"] = query
        st.session_state["exact"] = exact
        st.session_state["suggestions"] = suggestions
        st.query_params.update({"view": "results", "q": query})

    # Bookstore strip at bottom
    items = "".join(
        f'<div class="store-strip-item">📚 {store}</div>'
        for store in BOOKSTORES
    )
    st.markdown(
        f"""
        <div class="store-strip-container">
            <div class="store-strip-label">Searching across trusted bookstores</div>
            <div class="store-strip-badges">
                {items}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
