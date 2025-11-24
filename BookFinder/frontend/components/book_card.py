import streamlit as st
from utils.session import go_to_detail


def get_book_image(book_title: str) -> str:
    """
    Get a consistent book image based on the book title.
    Uses hash to randomly but consistently select from available images.
    
    Args:
        book_title: The title of the book
        
    Returns:
        Path to the image file
    """
    # We have 7 images: book_2, book_3, book_4, book_5, book_6, book_7, book_13
    available_images = [2, 3, 4, 5, 6, 7, 13]
    
    # Use hash of title to get consistent but random-looking selection
    title_hash = hash(book_title) if book_title else 0
    image_num = available_images[title_hash % len(available_images)]
    return f"img/book_{image_num}.jpg"


def render_book_card(book: dict, book_id: int = None, index: int = 0):
    """
    Render a book card with cover, title, author, description, and store info.
    """
    full_stars = int(round(book["rating"]))
    stars = "★" * full_stars + "☆" * (5 - full_stars)
    store = book["store"]

    # Get book image based on title (consistent but random-looking)
    book_image = get_book_image(book.get("title", ""))
    
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
        """,
        unsafe_allow_html=True,
    )
        
        # Add View button using Streamlit button (only if book_id is provided)
        if book_id is not None:
            if st.button("View", key=f"view_book_{book_id}_{index}", type="primary"):
                go_to_detail(book_id)
                st.rerun()
        
        st.markdown("""
                </div>
              </div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
