"""
Styles module for FindMyRead application.
Contains all CSS styling for the Streamlit app.
"""

from .base import get_base_styles
from .layout import get_layout_styles
from .navigation import get_navigation_styles
from .sidebar import get_sidebar_styles
from .forms import get_form_styles
from .hero import get_hero_styles
from .book_cards import get_book_card_styles
from .results import get_results_styles
from .detail import get_detail_styles
from .store_strip import get_store_strip_styles
from .responsive import get_responsive_styles


def get_styles():
    """Returns the complete CSS styles for the application."""
    return f"""
    <style>
    {get_base_styles()}
    {get_layout_styles()}
    {get_navigation_styles()}
    {get_sidebar_styles()}
    {get_form_styles()}
    {get_hero_styles()}
    {get_book_card_styles()}
    {get_results_styles()}
    {get_detail_styles()}
    {get_store_strip_styles()}
    {get_responsive_styles()}
    </style>
    """

