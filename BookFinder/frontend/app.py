"""
FindMyRead - Book Discovery Application
Main entry point for the Streamlit application.

This app helps users discover books across multiple Armenian bookstores.
"""
import streamlit as st
from config.settings import PAGE_TITLE, PAGE_ICON, LAYOUT
from styles.main_styles import get_styles
from utils.session import initialize_session_state, sync_query_params
from components.home import render_home
from components.results import render_results
from components.detail import render_detail


def main():
    """Main application entry point."""
    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)
    st.markdown(get_styles(), unsafe_allow_html=True)
    initialize_session_state()
    sync_query_params()
    
    # Render top bar (logo)
    st.markdown(
        '<div class="app-logo"><div class="logo-icon">F</div><span>FindMyRead</span></div>',
        unsafe_allow_html=True
    )
    
    # Route to appropriate view based on session state
    current_view = st.session_state["view"]
    
    if current_view == "home":
        render_home()
    elif current_view == "results":
        render_results()
    elif current_view == "detail":
        render_detail()
    else:
        # Fallback to home if invalid view
        st.session_state["view"] = "home"
        render_home()


if __name__ == "__main__":
    main()
