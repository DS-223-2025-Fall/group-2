"""
Form styles: buttons, text inputs, search forms.
"""

def get_form_styles():
    """Returns CSS for forms, buttons, and input fields."""
    return """
    /* Global button styling - all buttons beige with dark text */
    button, .stButton > button, button[kind="primary"], button[kind="secondary"] {
        background: var(--login-btn-bg) !important;
        color: var(--login-btn-text) !important;
        border: 1px solid var(--logo-border) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
    }
    
    button:hover, .stButton > button:hover, button[kind="primary"]:hover, button[kind="secondary"]:hover {
        background: var(--login-btn-hover) !important;
        color: var(--login-btn-text) !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.08) !important;
    }
    
    button:active, .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    }

    /* Fix BaseWeb container styling - must be flex */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 8px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    div[data-testid="stTextInput"] div[data-baseweb="base-input"] {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    /* Make all text inputs light background */
    div[data-testid="stTextInput"] input {
        background: var(--search-bg) !important;
        color: var(--search-text) !important;
        border-radius: 8px !important;
        border: 1.5px solid #d0c4b0 !important;
        padding: 0 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        outline: none !important;
        height: 52px !important;
        line-height: 1.5 !important;
        box-sizing: border-box !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        box-shadow: 0 0 0 2px rgba(127,106,77,0.15) !important;
        outline: none !important;
        border: 1.5px solid #b5a797 !important;
    }
    
    div[data-testid="stTextInput"] input:focus-visible {
        outline: none !important;
        box-shadow: 0 0 0 2px rgba(127,106,77,0.15) !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(127,106,77,0.6) !important;
    }

    /* Search button styling: compact with border */
    button[type="submit"] {
        background: #ffffff !important;
        color: var(--search-btn-text) !important;
        border: 1.5px solid #d0c4b0 !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.8rem !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
        box-shadow: none !important;
        margin: 0 !important;
        white-space: nowrap !important;
        height: 52px !important;
    }
    
    button[type="submit"]:hover {
        background: #f8f6f3 !important;
        border-color: #b5a797 !important;
        transform: translateY(0);
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    
    button[type="submit"]:active {
        transform: translateY(0);
        background: #f0ede8 !important;
        box-shadow: none !important;
    }

    /* Hide "Press Enter to submit form" helper text */
    [data-testid="stForm"] [data-testid="InputInstructions"] {
        display: none !important;
    }
    
    [data-testid="stForm"] div[class*="instructions"] {
        display: none !important;
    }

    /* Optional: remove extra spacing */
    div[data-testid="stTextInput"] {
        margin-bottom: 0;
    }
    """

