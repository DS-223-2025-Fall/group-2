"""
Authentication Component for BookFinder
Handles login button and user display.
"""
import streamlit as st
from config.settings import BACKEND_URL, API_ENDPOINTS
from utils.session import is_authenticated, get_user_info, logout


def render_auth_button():
    """
    **Render the authentication interface for the application.**

    Displays a login button for *unauthenticated users* and user information 
    along with a logout button for *authenticated users*. The UI elements are 
    intended to be placed in the sidebar or header for easy access.

    - If the user is logged in:
        - Shows a section with the user's **name** and **email**.
        - Provides a **logout button** that clears the session and refreshes the page.

    - If the user is not logged in:
        - Displays a **login prompt** with a button directing to the login page.
        - Encourages users to authenticate to access features like **rating** and **reviewing books**.
    """
    if is_authenticated():
        # User is logged in - show user info and logout button
        user = get_user_info()
        
        st.markdown("---")
        st.markdown("### 👤 Logged In")
        
        if user["name"]:
            st.markdown(f"**{user['name']}**")
        st.markdown(f"📧 {user['email']}")
        
        if st.button("🚪 Logout", width='stretch'):
            logout()
            st.success("✅ Logged out successfully!")
            st.rerun()
    else:
        # User is not logged in - show login button
        st.markdown("---")
        st.markdown("### 🔐 Authentication")
        st.markdown("Login to rate and review books!")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🔑 Go to Login", width='stretch', type="primary"):
            from utils.session import go_to_login
            go_to_login()
            st.rerun()


def render_inline_auth_message():
    """
    **Display an inline authentication notice for protected features.**

    This function is meant for areas where authentication is required, 
    such as **rating** or **review forms**. It informs *unauthenticated users* 
    that login is necessary to proceed and provides a direct **login link**.

    - If the user is not logged in:
        - Shows a **warning message** prompting login.
        - Renders a clickable **login link** using the backend authentication URL.
        - Returns *False* to indicate the user is not authenticated.

    - If the user is logged in:
        - Returns *True*, allowing access to the protected feature.
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
