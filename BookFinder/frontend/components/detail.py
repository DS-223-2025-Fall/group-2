"""
Book detail page component for FindMyRead application.
Displays comprehensive information about a selected book.
"""
import streamlit as st
from utils.search import get_book_by_id
from utils.session import go_back_to_results
from components.rating_widget import render_ratings_section


def get_book_image(book_id) -> str:
    """
    Get a consistent book image for a given book ID.
    Uses modulo to cycle through available images.
    
    Args:
        book_id: The ID of the book (can be int or str)
        
    Returns:
        Path to the image file
    """
    # Convert to int if it's a string
    if isinstance(book_id, str):
        book_id = int(book_id)
    
    # We have 13 images (book_1.jpg to book_13.jpg)
    image_num = ((book_id - 1) % 13) + 1
    return f"img/book_{image_num}.jpg"


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
    
    # Header with title and author - single container
    st.markdown(f"""
        <div class="detail-header">
            <div class="detail-title">{book['title']}</div>
            <div class="detail-author">by {book['author']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content: cover and metadata at left, long description at right
    left, right = st.columns([2, 5])
    
    with left:
        # Book cover with actual image
        book_image = get_book_image(book.get('id', 1))
        st.image(book_image, use_container_width=True)
        
        # Rating with stars
        full_stars = int(round(book["rating"]))
        stars = "★" * full_stars + "☆" * (5 - full_stars)
        st.markdown(f"""
            <div class="detail-meta">
                <span class="detail-stars">{stars}</span>
                <span>{book['rating']} / 5</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Store price info (without "Available at" text)
        st.markdown(f"""
            <div class="detail-meta" style="margin-top: 1.5rem;">
                <div style="font-size: 1.125rem; margin-top: 0.5rem;">{book['store']['name']}</div>
                <div style="font-size: 1.25rem; font-weight: 600; color: var(--book-price, #2c1810); margin-top: 0.25rem;">
                    {book['store']['price']} {book['store']['currency']}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with right:
        st.markdown(f"""
            <div class="detail-description">
                {book.get('long_description', book['description'])}
            </div>
        """, unsafe_allow_html=True)
    
    # Ratings section
    st.markdown("---")
    render_ratings_section(book['id'])
