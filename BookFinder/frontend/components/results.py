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
        # Update URL
        st.query_params["view"] = "results"
        st.query_params["q"] = query2
        st.rerun()

    # Get current results from session state
    exact = st.session_state["exact"]
    suggestions = st.session_state["suggestions"]
    query = st.session_state["last_query"]

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

    # Display book cards in a grid using columns
    books_to_show = exact if exact else suggestions
    
    # Display books in rows of 2 columns
    for i in range(0, len(books_to_show), 2):
        cols = st.columns(2)
        
        # First book in the row
        with cols[0]:
            render_book_card(books_to_show[i], books_to_show[i].get("id"), index=i)
        
        # Second book in the row (if exists)
        if i + 1 < len(books_to_show):
            with cols[1]:
                render_book_card(books_to_show[i + 1], books_to_show[i + 1].get("id"), index=i + 1)
    
    # Add bottom padding
    st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
