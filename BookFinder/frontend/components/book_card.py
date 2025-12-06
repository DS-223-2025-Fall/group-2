import streamlit as st
from utils.session import go_to_detail


def get_book_image(book_title: str) -> str:
    """
    **Get a consistent book image based on the book title.**

    Uses a hash function to select an image in a *pseudo-random but repeatable* way 
    from the available set of book cover images. This ensures that the same book 
    always gets the same image.

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
    **Render a book card UI in Streamlit with cover, metadata, description, and store info.**

    The card can be fully *clickable* when a `book_id` is provided. Displays information 
    such as title, author, language, description, and pricing from the store. Highlights 
    the match type using colored badges (*Exact Match*, *Close Match*, *Similar Book*).

    - Clickable behavior:
        - If `book_id` is given, the card contains a hidden button that triggers 
          navigation to the book detail page.
    - Non-clickable behavior:
        - Shows the same visual layout without interaction.

    Args:
        book (dict): A dictionary containing book fields such as:
            - title (str)
            - author (str)
            - description (str)
            - language (str)
            - store (dict with keys "name", "price", "currency")
            - match_type (str): "exact", "fuzzy", or "semantic"
        book_id (int | None): If provided, makes the card clickable and
            opens the detailed view when clicked.
        index (int): Unique index used internally to generate Streamlit
            button keys and avoid collisions.

    Returns:
        None: This function renders UI components directly in Streamlit
        and does not return a value.
    """
    store = book["store"]

    # Get book image based on title (consistent but random-looking)
    book_image = get_book_image(book.get("title", ""))
    
    # Get language display - use as-is from database
    language = book.get("language", "")
    
    # Handle language display
    if language and language.strip():
        # Remove "Unknown" and empty values
        if language.strip().lower() not in ["unknown", ""]:
            # Take only the first language if multiple are listed
            language_display = language.split(",")[0].strip()
        else:
            language_display = ""
    else:
        language_display = ""
    
    # Determine badge text and color based on match type
    badge_html = ""
    match_type = book.get("match_type", "").lower()
    
    if match_type == "exact":
        badge_html = '<span style="font-size: 0.7rem; color: #28a745; margin-left: 8px;">• Exact Match</span>'
    elif match_type == "fuzzy":
        badge_html = '<span style="font-size: 0.7rem; color: #ffc107; margin-left: 8px;">• Close Match</span>'
    elif match_type == "semantic":
        badge_html = '<span style="font-size: 0.7rem; color: #17a2b8; margin-left: 8px;">• Similar Book</span>'
    
    # Clickable card
    if book_id is not None:
        # Wrap everything in a container for relative positioning
        with st.container():
            # Create columns for layout
            col1, col2 = st.columns([1, 4])
            
            with col1:
                st.image(book_image, width='stretch')
            
            with col2:
                # Build author line with language if available
                author_line = f"by {book['author']}"
                if language_display:
                    author_line += f" • {language_display}"
                
                st.markdown(f"""
                <div class="book-card-content">
                    <div class="book-title">{book['title']}{badge_html}</div>
                    <div class="book-author">{author_line}</div>
                    <div class="book-desc">{book['description']}</div>
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
                """, unsafe_allow_html=True)
                
                # Hidden button inside the content column to make card clickable
                if st.button("​", key=f"card_btn_{book_id}_{index}", type="secondary"):
                    go_to_detail(book_id)
                    st.rerun()
    else:
        # Non-clickable card
        col1, col2 = st.columns([1, 4])
        
        with col1:
            st.image(book_image, width='stretch')
        
        with col2:
            # Build author line with language if available
            author_line = f"by {book['author']}"
            if language_display:
                author_line += f" • {language_display}"
            
            st.markdown(f"""
            <div class="book-card-content">
                <div class="book-title">{book['title']}{badge_html}</div>
                <div class="book-author">{author_line}</div>
                <div class="book-desc">{book['description']}</div>
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
            """, unsafe_allow_html=True)
