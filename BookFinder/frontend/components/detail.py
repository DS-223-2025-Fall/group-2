"""
Book detail page component for FindMyRead application.
Displays comprehensive information about a selected book.
"""
import streamlit as st
from utils.search import get_book_by_id
from utils.session import go_back_to_results
# Add this import at the top
from components.rating_widget import render_ratings_section

# Inside render_detail(), after displaying book description, add:
   


def render_detail():
    """Render the book detail page."""
    selected_id = st.session_state.get("selected_book_id")
    book = get_book_by_id(selected_id)
    
    if book is None:
        st.warning("Book not found.")
        go_back_to_results()
        return
    
    # Back button
    if st.button("← Back to Results", key="detail_back"):
        go_back_to_results()
    
    # Header with title and author
    st.markdown(f"""
        <div class="detail-header">
            <div class="detail-title">{book['title']}</div>
            <div class="detail-author">by {book['author']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content: cover and metadata at left, long description at right
    st.markdown('<div class="detail-content">', unsafe_allow_html=True)
    left, right = st.columns([2, 5])
    
    with left:
        # Book cover
        st.markdown('<div class="detail-cover"></div>', unsafe_allow_html=True)
        
        # Rating with stars
        full_stars = int(round(book["rating"]))
        stars = "★" * full_stars + "☆" * (5 - full_stars)
        st.markdown(f"""
            <div class="detail-meta">
                <span class="detail-stars">{stars}</span>
                <span>{book['rating']} / 5</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Store info
        st.markdown(f"""
            <div class="detail-meta" style="margin-top: 1.5rem;">
                <div class="detail-meta-label">Available at:</div>
                <div style="font-size: 1.125rem; margin-top: 0.5rem;">{book['store']['name']}</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: var(--book-price, #2c1810); margin-top: 0.25rem;">
                    {book['store']['price']} {book['store']['currency']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Buy button
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("Buy from Store", key=f"buy_{book.get('id')}", use_container_width=True):
            st.info(f"This would redirect to {book['store']['name']} in a real app.")
    
    with right:
        st.markdown(f"""
            <div class="detail-description">
                {book.get('long_description', book['description'])}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ratings section
    st.markdown("---")
    render_ratings_section(book['id'])
