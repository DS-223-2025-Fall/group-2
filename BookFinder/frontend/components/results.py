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
                "Search query",
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

    # Separate based on match_type:
    # - Exact and Fuzzy matches go to "Found in Bookstores"
    # - Semantic matches (including recommendations) go to "You Might Also Like"
    found_in_stores = [
        book for book in exact 
        if book.get("match_type") in ["exact", "fuzzy"]
    ]
    
    similar_books = [
        book for book in exact 
        if book.get("match_type") == "semantic" or book.get("is_recommendation", False)
    ]
    
    # Display "Found in Bookstores" section if we have exact or fuzzy matches
    if found_in_stores:
        st.markdown('<div class="results-header">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">Found in Bookstores</div>', unsafe_allow_html=True)
        count_text = f"{len(found_in_stores)} result" + ("s" if len(found_in_stores) != 1 else "")
        st.markdown(
            f'<div class="result-subtitle">{count_text} for "{query}"</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display books in rows of 2 columns
        for i in range(0, len(found_in_stores), 2):
            cols = st.columns(2)
            
            with cols[0]:
                render_book_card(found_in_stores[i], found_in_stores[i].get("id"), index=i)
            
            if i + 1 < len(found_in_stores):
                with cols[1]:
                    render_book_card(found_in_stores[i + 1], found_in_stores[i + 1].get("id"), index=i + 1)
    
    # Display "You Might Also Like" section for semantic matches
    if similar_books:
        # Add spacing if we already showed "Found in Bookstores"
        if found_in_stores:
            st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="results-header">', unsafe_allow_html=True)
        
        # Different title/subtitle based on whether we found exact/fuzzy matches
        if found_in_stores:
            st.markdown('<div class="result-title">You Might Also Like</div>', unsafe_allow_html=True)
            st.markdown('<div class="result-subtitle">Similar books based on your search</div>', unsafe_allow_html=True)
        else:
            # Only semantic matches, no exact/fuzzy found
            st.markdown('<div class="result-title">Not Found in Bookstores</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="result-subtitle">We couldn\'t find "{query}" in our bookstores, but here are similar books</div>',
                unsafe_allow_html=True,
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display semantic books in rows of 2 columns
        for i in range(0, len(similar_books), 2):
            cols = st.columns(2)
            
            with cols[0]:
                render_book_card(similar_books[i], similar_books[i].get("id"), index=i + 1000)
            
            if i + 1 < len(similar_books):
                with cols[1]:
                    render_book_card(similar_books[i + 1], similar_books[i + 1].get("id"), index=i + 1001)
    
    # If no results at all, show fallback suggestions
    if not found_in_stores and not similar_books:
        st.markdown('<div class="results-header">', unsafe_allow_html=True)
        st.markdown('<div class="result-title">No Results Found</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="result-subtitle">We couldn\'t find any books matching "{query}"</div>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show fallback suggestions if available
        if suggestions:
            st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)
            st.markdown('<div class="result-subtitle">You might like these books:</div>', unsafe_allow_html=True)
            
            for i in range(0, len(suggestions), 2):
                cols = st.columns(2)
                
                with cols[0]:
                    render_book_card(suggestions[i], suggestions[i].get("id"), index=i + 2000)
                
                if i + 1 < len(suggestions):
                    with cols[1]:
                        render_book_card(suggestions[i + 1], suggestions[i + 1].get("id"), index=i + 2001)
    
    # Add bottom padding
    st.markdown('<div style="height: 3rem;"></div>', unsafe_allow_html=True)
