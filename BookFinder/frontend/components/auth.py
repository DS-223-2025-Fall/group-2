"""
Authentication Component for BookFinder
Handles login button and user display.
"""
import streamlit as st
from config.settings import BACKEND_URL, API_ENDPOINTS
from utils.session import is_authenticated, get_user_info, logout


def render_auth_button():
    """
    Render authentication UI in the sidebar or header.
    Shows login button if not authenticated, user info if authenticated.
    """
    if is_authenticated():
        # User is logged in - show user info and logout button
        user = get_user_info()
        
        st.markdown("---")
        st.markdown("### 👤 Logged In")
        
        if user["name"]:
            st.markdown(f"**{user['name']}**")
        st.markdown(f"📧 {user['email']}")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.success("✅ Logged out successfully!")
            st.rerun()
    else:
        # User is not logged in - show login button
        st.markdown("---")
        st.markdown("### 🔐 Authentication")
        st.markdown("Login to rate and review books!")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔑 Go to Login", use_container_width=True, type="primary"):
            from utils.session import go_to_login
            go_to_login()
            st.rerun()


def render_inline_auth_message():
    """
    Render inline authentication message for protected features.
    Use this in places like rating forms.
    """
    if not is_authenticated():
        st.warning("🔒 Please login to rate books")
        
        # Create login URL
        login_url = f"{BACKEND_URL}{API_ENDPOINTS['auth_google']}"
        
        st.markdown(
            f'<a href="{login_url}" target="_self">🔑 Login with Google</a>',
            unsafe_allow_html=True
        )
        return False
    return True
