"""
Rating Widget Component for BookFinder
Handles displaying ratings and submitting new ratings.
"""
import streamlit as st
from typing import List, Dict, Optional
from utils.api_client import APIClient
from utils.session import is_authenticated, get_auth_token, get_user_info


def render_star_rating(rating: float, max_stars: int = 5, size: int = 20) -> str:
    """
    Generate HTML for star rating display.
    
    Args:
        rating: Rating value (0-5)
        max_stars: Maximum number of stars
        size: Size of stars in pixels
        
    Returns:
        HTML string for stars
    """
    full_stars = int(rating)
    partial_star = rating - full_stars
    empty_stars = max_stars - full_stars - (1 if partial_star > 0 else 0)
    
    html = f'<div style="color: #FFD700; font-size: {size}px; line-height: 1;">'
    
    # Full stars
    html += '★' * full_stars
    
    # Partial star
    if partial_star > 0:
        html += '★'  # For now, show full star if there's any partial
    
    # Empty stars
    html += '☆' * empty_stars
    
    html += f' <span style="color: #666; font-size: {size-2}px;">({rating:.1f})</span>'
    html += '</div>'
    
    return html


def render_rating_submission(book_id: str) -> None:
    """
    Render the rating submission form.
    
    Args:
        book_id: The book's unique identifier
    """
    st.markdown("### 📝 Rate This Book")
    
    # Check if user is authenticated
    if not is_authenticated():
        st.warning("🔒 Please login to rate books")
        
        if st.button("🔑 Go to Login Page", use_container_width=True, type="primary"):
            from utils.session import go_to_login
            go_to_login()
            st.rerun()
        return
    
    # Show logged in user info
    user = get_user_info()
    st.info(f"📧 Posting as: {user['email']}")
    
    # Show success message if rating was just submitted
    if st.session_state.get('rating_submitted', False):
        st.success("✅ Thank you for your rating!")
        st.session_state['rating_submitted'] = False
    
    with st.form(key=f"rating_form_{book_id}"):
        # Star rating selector - discrete options
        st.markdown("**Your Rating**")
        rating = st.radio(
            "Select your rating",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: '⭐' * x + f' ({x} star{"s" if x > 1 else ""})',
            index=None,  # No default selection
            label_visibility="collapsed",
            horizontal=False
        )
        
        # Comment text area
        comment = st.text_area(
            "Your Review (optional)",
            placeholder="Share your thoughts about this book...",
            max_chars=500,
            height=100
        )
        
        # Submit button
        submitted = st.form_submit_button("Submit Rating", type="primary")
        
        if submitted:
            if rating is None:
                st.error("⚠️ Please select a rating (1-5 stars)")
            else:
                # Submit the rating with authentication token
                api_client = APIClient(auth_token=get_auth_token())
                result = api_client.rate_book(
                    book_id=book_id,
                    rating=rating,
                    comment=comment if comment.strip() else None
                )
                
                if result:
                    # Store success state to show message after rerun
                    st.session_state['rating_submitted'] = True
                    st.rerun()
                else:
                    st.error("❌ Failed to submit rating. Please try again.")


def render_ratings_list(ratings: List[Dict]) -> None:
    """
    Display a list of existing ratings.
    
    Args:
        ratings: List of rating dictionaries
    """
    if not ratings:
        st.info("🔍 No ratings yet. Be the first to rate this book!")
        return
    
    st.markdown(f"### 💬 User Reviews ({len(ratings)})")
    
    # Calculate average rating
    avg_rating = sum(r["rating"] for r in ratings) / len(ratings)
    
    # Display average
    st.markdown("#### Average Rating")
    st.markdown(render_star_rating(avg_rating, size=24), unsafe_allow_html=True)
    st.markdown("---")
    
    # Display individual ratings
    for idx, rating in enumerate(ratings):
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                # User email (anonymized)
                email = rating.get("user_email", "Anonymous")
                # Show only first part of email for privacy
                display_email = email.split('@')[0] + "@***" if '@' in email else "Anonymous"
                st.markdown(f"**{display_email}**")
            
            with col2:
                # Star rating
                st.markdown(
                    render_star_rating(rating["rating"], size=16), 
                    unsafe_allow_html=True
                )
            
            # Comment
            if rating.get("comment"):
                st.markdown(f'> {rating["comment"]}')
            
            # Divider between reviews (except last one)
            if idx < len(ratings) - 1:
                st.markdown("---")


def render_ratings_section(book_id: str) -> None:
    """
    Render complete ratings section (list + submission form).
    
    Args:
        book_id: The book's unique identifier
    """
    # Fetch existing ratings
    api_client = APIClient()
    ratings = api_client.get_book_ratings(book_id)
    
    # Create tabs for viewing and submitting
    tab1, tab2 = st.tabs(["📚 View Ratings", "✍️ Rate This Book"])
    
    with tab1:
        if ratings is not None:
            render_ratings_list(ratings)
        else:
            st.error("❌ Failed to load ratings. Please try again later.")
    
    with tab2:
        render_rating_submission(book_id)
