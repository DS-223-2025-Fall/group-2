"""
Book detail page component for FindMyRead application.
Displays comprehensive information about a selected book.
"""
import streamlit as st
from utils.search import get_book_by_id
from utils.session import go_back_to_home, go_home
from components.rating_widget import render_ratings_section


def get_book_image(book_title: str) -> str:
    """
    **Get a consistent book image based on the book title.**

    Uses a hash function to select an image in a *pseudo-random but repeatable* way 
    from the available set of book cover images. Ensures that the same book always 
    receives the same image, providing visual consistency across the app.

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


def render_detail():
    """
    **Render the book detail page in Streamlit.**

    Displays comprehensive information for a selected book, including:

    - Header with **title**, **author**, and *primary language*.
    - Main section with book **cover image** and **pricing info** from the store.
    - Long **description** or plot summary.
    - Ratings section showing user reviews and interactive rating widgets.

    Provides a **back button** to navigate to previous results or home, 
    depending on the user's navigation history.
    """
    selected_id = st.session_state.get("selected_book_id")
    book = get_book_by_id(selected_id)
    
    if book is None:
        st.warning("Book not found.")
        go_back_to_home()
        return
    
    # Back button - go to results if we have a search query, otherwise home
    last_query = st.session_state.get("last_query", "")
    has_results = st.session_state.get("exact") or st.session_state.get("suggestions")
    
    if last_query and has_results:
        back_label = "← Back to Results"
    else:
        back_label = "← Back to Home"
    
    if st.button(back_label, key="detail_back"):
        if last_query and has_results:
            # Go back to results
            st.session_state["view"] = "results"
            st.query_params["view"] = "results"
            st.query_params["q"] = last_query
        else:
            # Go back to home
            go_home()
        st.rerun()
    
    # Header with title and author
    # Get language for display
    language = book.get("language", "")
    if language and language.strip() and language.strip().lower() not in ["unknown", ""]:
        language_display = language.split(",")[0].strip()
        author_info = f"by {book['author']} • {language_display}"
    else:
        author_info = f"by {book['author']}"
    
    st.markdown(f"""
        <div class="detail-header">
            <div class="detail-title">{book['title']}</div>
            <div class="detail-author">{author_info}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Main content: cover and metadata at left, long description at right
    left, right = st.columns([2, 5])
    
    with left:
        # Book cover with actual image
        book_image = get_book_image(book.get('title', ''))
        st.image(book_image, width='stretch')
        
        # # Rating with stars - show "No reviews yet" if rating is 4.0 (default)
        # rating = book.get("rating", 4.0)
        # if rating == 4.0:  # Default rating means no real reviews
        #     stars = "☆" * 5
        #     st.markdown(f"""
        #         <div class="detail-meta">
        #             <span class="detail-stars">{stars}</span>
        #             <span style="color: #999;">No reviews yet</span>
        #         </div>
        #     """, unsafe_allow_html=True)
        # else:
        #     # Show actual rating
        #     full_stars = int(round(rating))
        #     stars = "★" * full_stars + "☆" * (5 - full_stars)
        #     st.markdown(f"""
        #         <div class="detail-meta">
        #             <span class="detail-stars">{stars}</span>
        #             <span>{rating} / 5</span>
        #         </div>
        #     """, unsafe_allow_html=True)
        
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
