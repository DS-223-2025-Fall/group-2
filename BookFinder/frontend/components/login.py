"""
Login page component for BookFinder
Dedicated page for user authentication.
"""
import streamlit as st
from config.settings import BACKEND_BROWSER_URL, API_ENDPOINTS
from utils.session import is_authenticated, get_user_info


def render_login():
    """Render the login page."""
    # If already authenticated, show welcome message
    if is_authenticated():
        user = get_user_info()
        
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem 0;">
                <h1>✅ You're Already Logged In!</h1>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.success(f"Welcome back, **{user['name'] or user['email']}**!")
            st.info(f"📧 {user['email']}")
            
            st.markdown("---")
            
            # Navigation buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("🏠 Go to Home", width='stretch', type="primary"):
                    from utils.session import go_home
                    go_home()
                    st.rerun()
            
            with col_b:
                if st.button("🚪 Logout", width='stretch'):
                    from utils.session import logout
                    logout()
                    st.success("✅ Logged out successfully!")
                    st.rerun()
        
        return
    
    # Not authenticated - show login page
    st.markdown(
        """
        <div class="hero-wrapper fade-in">
            <div class="hero-title">Login to<br/>FindMyRead</div>
            <div class="hero-subtitle">
                Sign in to rate books, write reviews, and save your favorites
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Center the login card
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info("🔒 We use Google OAuth for secure authentication. We only access your email and name.")
        
        # Create login URL (use BACKEND_BROWSER_URL for browser redirects)
        login_url = f"{BACKEND_BROWSER_URL}{API_ENDPOINTS['auth_google']}"
        
        # Google Sign In Button (styled)
        st.markdown(
            f"""
            <a href="{login_url}" target="_self" style="
                display: block;
                padding: 1rem;
                background: linear-gradient(135deg, #4285f4 0%, #34a853 100%);
                color: white;
                text-decoration: none;
                border-radius: 0.5rem;
                font-weight: 600;
                text-align: center;
                font-size: 1.1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                transition: transform 0.2s;
            " onmouseover="this.style.transform='scale(1.05)'" 
               onmouseout="this.style.transform='scale(1)'">
                🔑 Continue with Google
            </a>
            """,
            unsafe_allow_html=True
        )
        
        # Back to home button
        st.markdown("<br/>", unsafe_allow_html=True)
        if st.button("← Back to Home", width='stretch'):
            from utils.session import go_home
            go_home()
            st.rerun()
        
        # Privacy notice
        st.markdown(
            """
            <div style="text-align: center; margin-top: 2rem; color: #7f6a4d; font-size: 0.9rem;">
                By signing in, you agree to our Terms of Service and Privacy Policy.<br/>
                Your data is secure and we never share your information.
            </div>
            """,
            unsafe_allow_html=True
        )
