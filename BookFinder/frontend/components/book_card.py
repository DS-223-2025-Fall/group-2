import streamlit as st


def get_book_image(book_id: int) -> str:
    """
    Get a consistent book image for a given book ID.
    Uses modulo to cycle through available images.
    
    Args:
        book_id: The ID of the book
        
    Returns:
        Path to the image file
    """
    # We have 13 images (book_1.jpg to book_13.jpg)
    image_num = ((book_id - 1) % 13) + 1
    return f"img/book_{image_num}.jpg"


def render_book_card(book: dict, book_id: int = None, index: int = 0):
    """
    Render a book card with cover, title, author, description, and store info.
    """
    full_stars = int(round(book["rating"]))
    stars = "★" * full_stars + "☆" * (5 - full_stars)
    store = book["store"]

    # Build optional View button HTML (only if book_id is provided)
    view_button_html = ""
    if book_id is not None:
        view_button_html = f'<div class="book-view-btn-wrapper"><a href="?book_id={book_id}" class="book-view-btn">View</a></div>'

    # Get book image
    book_image = get_book_image(book_id if book_id else 1)
    
    st.markdown(
        f"""
        <div class="book-card-container">
          <div class="book-card">
            <div class="book-card-inner">
        """,
        unsafe_allow_html=True,
    )
    
    # Display actual book image using Streamlit's image widget
    col_img, col_content = st.columns([1, 4])
    with col_img:
        st.image(book_image, use_container_width=True)
    
    with col_content:
        st.markdown(f"""
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
                  {view_button_html}
                </div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
