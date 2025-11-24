"""
Search results page component for FindMyRead application.
Displays search results with book cards.
"""
import streamlit as st
from components.book_card import render_book_card
from utils.search import simple_search
from utils.session import go_home


def render_results():
    """Render the search results page."""
    # Search bar with back button
    with st.form("results_search"):
        col_back, col_input, col_btn = st.columns([0.7, 7, 2])

        with col_back:
            back_clicked = st.form_submit_button("←")

        with col_input:
            query2 = st.text_input(
                "",
                value=st.session_state["last_query"],
                label_visibility="collapsed",
                key="results_query",
            )

        with col_btn:
            search_again = st.form_submit_button("Search")

    # Handle navigation
    if back_clicked:
        go_home()
        st.rerun()

    if search_again and query2:
        exact, suggestions = simple_search(query2)
        st.session_state["last_query"] = query2
        st.session_state["exact"] = exact
        st.session_state["suggestions"] = suggestions
        st.query_params.update({"view": "results", "q": query2})
        st.rerun()

    # Get current results from session state
    exact = st.session_state.get("exact", [])
    suggestions = st.session_state.get("suggestions", [])
    query = st.session_state.get("last_query", "")
    
    # If no results at all, redirect to home to search again
    if not exact and not suggestions:
        st.info("No search results found. Please search for a book.")
        if st.button("Go to Home"):
            go_home()
            st.rerun()
        return

    # Header text
    st.markdown('<div class="results-header">', unsafe_allow_html=True)
    if exact:
        st.markdown('<div class="result-title">Found in Bookstores</div>', unsafe_allow_html=True)
        count_text = f"{len(exact)} result" + ("s" if len(exact) != 1 else "")
        st.markdown(
            f'<div class="result-subtitle">{count_text} for "{query}"</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="result-title">You Might Like These</div>', unsafe_allow_html=True)
        subtitle_text = f'We couldn\'t find an exact match for "{query}", but here are some similar books'
        st.markdown(
            f'<div class="result-subtitle">{subtitle_text}</div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Display book cards
    if exact:
        # Center exact match cards with consistent container
        st.markdown('<div class="exact-results-container">', unsafe_allow_html=True)
        for idx, book in enumerate(exact):
            render_book_card(book, book.get("id"), index=idx)
            if idx < len(exact) - 1:
                st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Grid layout for suggestions
        st.markdown('<div class="recommend-grid">', unsafe_allow_html=True)
        for idx, book in enumerate(suggestions):
            st.markdown("<div>", unsafe_allow_html=True)
            render_book_card(book, book.get("id"), index=idx)
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
