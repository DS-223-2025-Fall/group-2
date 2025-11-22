"""
Book card component - reusable UI element for displaying book information.
"""
import streamlit as st
from utils.session import go_to_detail


def render_book_card(book: dict, book_id: int = None):
    """
    Render a book card with cover, title, author, description, and store info.
    
    Args:
        book: Book dictionary containing book data
        book_id: Optional book ID for adding a View button
    """
    # Calculate star rating display
    full_stars = int(round(book["rating"]))
    stars = "★" * full_stars + "☆" * (5 - full_stars)
    store = book["store"]
    
    # Render book card HTML
    html = f"""
    <div class="book-card">
      <div class="book-card-inner">
        <div class="book-cover"></div>
        <div class="book-main">
          <div class="book-title">{book['title']}</div>
          <div class="book-author">by {book['author']}</div>
          <div class="book-desc">{book['description']}</div>
          <div class="book-rating-row">
            <span class="book-stars">{stars}</span>
            <span class="book-rating-value">{book['rating']}</span>
          </div>
          <div class="book-bottom-row">
            <div class="book-store-pill">
              <span class="book-store-icon"></span>
              <span>
                <span class="book-store-name">{store['name']}</span>
                <span class="book-price">{store['price']} {store['currency']}</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # Add View button if book_id provided
    if book_id is not None:
        c1, c2, c3 = st.columns([6, 1, 1])
        with c2:
            st.button("View", key=f"view_{book_id}", on_click=go_to_detail, args=(book_id,))
