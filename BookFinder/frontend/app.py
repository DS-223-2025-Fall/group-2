"""
FindMyRead - Book Discovery Application
Main entry point for the Streamlit application.

This app helps users discover books across multiple Armenian bookstores.
"""
import streamlit as st
from urllib.parse import unquote
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT
from styles.main_styles import get_styles
from utils.session import initialize_session_state, sync_query_params, login, is_authenticated
from components.home import render_home
from components.results import render_results
from components.detail import render_detail
from components.login import render_login
from components.auth import render_auth_button


def handle_auth_callback():
    """Handle authentication callback from Google OAuth."""
    query_params = st.query_params
    
    # Check if we have auth token in URL (from OAuth callback)
    if "token" in query_params and not is_authenticated():
        token = query_params["token"]
        email = unquote(query_params.get("email", ""))
        name = unquote(query_params.get("name", ""))
        
        # Store in session
        login(token, email, name)
        
        # Clean URL by removing auth params
        st.query_params.clear()
        st.success(f"✅ Welcome, {name or email}!")
        st.rerun()


def main():
    """Main application entry point."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)
    st.markdown(get_styles(), unsafe_allow_html=True)
    initialize_session_state()
    
    # Handle OAuth callback first
    handle_auth_callback()
    
    # Then sync other query params
    sync_query_params()
    
    # Render top bar with logo and auth
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            '<div class="app-logo"><div class="logo-icon">F</div><span>FindMyRead</span></div>',
            unsafe_allow_html=True
        )
    
    with col2:
        # Show auth status in header (compact view)
        if is_authenticated():
            from utils.session import get_user_info
            user = get_user_info()
            st.markdown(f"👤 {user['name'] or user['email']}")
        else:
            if st.button("🔑 Login", key="header_login"):
                from utils.session import go_to_login
                go_to_login()
                st.rerun()
    
    # Sidebar for detailed auth info
    with st.sidebar:
        render_auth_button()
    
    # Route to appropriate view based on session state
    current_view = st.session_state["view"]
    
    if current_view == "home":
        render_home()
    elif current_view == "results":
        render_results()
    elif current_view == "detail":
        render_detail()
    elif current_view == "login":
        render_login()
    else:
        # Fallback to home if invalid view
        st.session_state["view"] = "home"
        render_home()


if __name__ == "__main__":
    main()
